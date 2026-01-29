from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.core.db import get_db
from app.models.bot import Bot
from app.schemas.bot import BotCreate, BotOut

router = APIRouter(tags=["bots"])


@router.get("/admin/bots", response_model=list[BotOut], dependencies=[Depends(get_current_admin)])
def list_bots(db: Session = Depends(get_db)):
    return db.scalars(select(Bot).order_by(Bot.id.desc())).all()


@router.post("/admin/bots", response_model=BotOut, status_code=201, dependencies=[Depends(get_current_admin)])
def create_bot(payload: BotCreate, db: Session = Depends(get_db)):
    b = Bot(name=payload.name, token=payload.token, is_active=True)
    db.add(b)
    db.commit()
    db.refresh(b)
    return b


@router.post("/admin/bots/{bot_id}/toggle", response_model=BotOut, dependencies=[Depends(get_current_admin)])
def toggle_bot(bot_id: int, db: Session = Depends(get_db)):
    b = db.get(Bot, bot_id)
    if not b:
        raise HTTPException(404, "Bot not found")
    b.is_active = not b.is_active
    db.commit()
    db.refresh(b)
    return b
