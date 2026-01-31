from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models.user import User
from app.schemas.user import UserOut, UserUpsert
from app.api.deps import get_current_admin

router = APIRouter(tags=["users"])


@router.post("/bot/users/upsert", response_model=UserOut)
def bot_upsert_user(payload: UserUpsert, db: Session = Depends(get_db)):
    now = datetime.now(timezone.utc)

    user = db.scalar(select(User).where(User.tg_id == payload.tg_id))
    if not user:
        user = User(
            tg_id=payload.tg_id,
            username=payload.username,
            first_name=payload.first_name,
            phone=payload.phone,
            source=payload.source,
            is_blocked=False,
            created_at=now,
            last_seen_at=now,
        )
        db.add(user)
    else:
        if payload.username is not None:
            user.username = payload.username
        if payload.first_name is not None:
            user.first_name = payload.first_name
        if payload.phone is not None:
            user.phone = payload.phone
        if payload.source is not None:
            user.source = payload.source
        user.last_seen_at = now

    db.commit()
    db.refresh(user)
    return user


@router.get("/admin/users", response_model=list[UserOut], dependencies=[Depends(get_current_admin)])
def admin_list_users(db: Session = Depends(get_db)):
    return db.scalars(select(User).order_by(User.id.desc())).all()
