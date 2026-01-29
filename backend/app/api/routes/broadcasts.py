from __future__ import annotations

import asyncio
from datetime import datetime, timezone

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.core.db import get_db, SessionLocal
from app.core.telegram import tg_send_message, TelegramError
from app.models.broadcast import Broadcast
from app.models.broadcast_log import BroadcastLog
from app.models.bot import Bot
from app.models.user import User
from app.schemas.broadcast import BroadcastCreate, BroadcastOut

router = APIRouter(tags=["broadcasts"])


@router.post("/admin/broadcasts", response_model=BroadcastOut, status_code=201, dependencies=[Depends(get_current_admin)])
def create_broadcast(payload: BroadcastCreate, db: Session = Depends(get_db)):
    now = datetime.now(timezone.utc)
    b = Broadcast(text=payload.text, status="draft", created_at=now)
    db.add(b)
    db.commit()
    db.refresh(b)
    return b


@router.get("/admin/broadcasts", response_model=list[BroadcastOut], dependencies=[Depends(get_current_admin)])
def list_broadcasts(db: Session = Depends(get_db)):
    return db.scalars(select(Broadcast).order_by(Broadcast.id.desc())).all()


@router.post("/admin/broadcasts/{broadcast_id}/start", response_model=BroadcastOut, dependencies=[Depends(get_current_admin)])
def start_broadcast(broadcast_id: int, background: BackgroundTasks, db: Session = Depends(get_db)):
    bc = db.get(Broadcast, broadcast_id)
    if not bc:
        raise HTTPException(404, "Broadcast not found")

    if bc.status in ("sending", "done"):
        return bc

    bc.status = "sending"
    bc.started_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(bc)

    # запускаем в фоне (отдельная сессия внутри)
    background.add_task(run_broadcast_job, broadcast_id)
    return bc


async def run_broadcast_job(broadcast_id: int) -> None:
    """
    ВАЖНО: это MVP-фоновая задача.
    Для прод-уровня лучше очередь (Celery/RQ/Arq), но для портфолио — ок.
    """
    # отдельная DB-сессия
    db: Session = SessionLocal()
    try:
        bc = db.get(Broadcast, broadcast_id)
        if not bc:
            return

        bots = db.scalars(select(Bot).where(Bot.is_active == True).order_by(Bot.id.asc())).all()
        if not bots:
            bc.status = "done"
            bc.finished_at = datetime.now(timezone.utc)
            db.commit()
            return

        users = db.scalars(select(User).where(User.is_blocked == False).order_by(User.id.asc())).all()

        idx = 0
        for u in users:
            bot = bots[idx % len(bots)]
            idx += 1

            now = datetime.now(timezone.utc)

            try:
                await tg_send_message(bot.token, u.tg_id, bc.text)

                db.add(BroadcastLog(
                    broadcast_id=bc.id,
                    user_id=u.id,
                    bot_id=bot.id,
                    status="ok",
                    error_text=None,
                    attempt=1,
                    created_at=now,
                ))
                db.commit()

            except TelegramError as e:
                # типовые реакции
                err = str(e)
                code = getattr(e, "code", None)

                # user blocked / chat not found → помечаем пользователя
                if code in (403, 400) and ("blocked" in err.lower() or "chat not found" in err.lower()):
                    u.is_blocked = True

                # unauthorized → бот “умер”
                if code == 401 or "unauthorized" in err.lower():
                    bot.is_active = False
                    # обновляем список активных ботов
                    bots = db.scalars(select(Bot).where(Bot.is_active == True).order_by(Bot.id.asc())).all()
                    if not bots:
                        # больше некем слать
                        db.add(BroadcastLog(
                            broadcast_id=bc.id,
                            user_id=u.id,
                            bot_id=bot.id,
                            status="error",
                            error_text="No active bots left",
                            attempt=1,
                            created_at=now,
                        ))
                        db.commit()
                        break

                db.add(BroadcastLog(
                    broadcast_id=bc.id,
                    user_id=u.id,
                    bot_id=bot.id,
                    status="error",
                    error_text=err[:1000],
                    attempt=1,
                    created_at=now,
                ))
                db.commit()

            # анти-флуд: небольшая пауза
            await asyncio.sleep(0.05)

        bc.status = "done"
        bc.finished_at = datetime.now(timezone.utc)
        db.commit()

    finally:
        db.close()
