from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models.user import User
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderOut, OrderStatusUpdate
from app.api.deps_bot_admin import bot_admin_guard

router = APIRouter(tags=["orders"])


@router.post("/bot/orders", response_model=OrderOut)
def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.tg_id == payload.tg_id))
    if not user:
        raise HTTPException(404, "User not found (call /bot/users/upsert first)")

    # запрет второй заявки, если есть открытая
    open_order = db.scalar(
        select(Order).where(Order.user_id == user.id, Order.status.in_(["new", "in_progress"]))
    )
    if open_order:
        raise HTTPException(409, "You already have an active order")

    now = datetime.now(timezone.utc)
    o = Order(
        user_id=user.id,
        text=payload.text.strip(),
        phone=payload.phone.strip() if payload.phone else None,
        status="new",
        created_at=now,
        updated_at=now,
    )
    db.add(o)
    db.commit()
    db.refresh(o)
    return o


@router.get("/bot/orders/my", response_model=list[OrderOut])
def my_orders(tg_id: int, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.tg_id == tg_id))
    if not user:
        return []
    return db.scalars(select(Order).where(Order.user_id == user.id).order_by(Order.id.desc())).all()


# --- Админские (для бота) ---
@router.get("/bot/admin/orders", response_model=list[OrderOut], dependencies=[Depends(bot_admin_guard)])
def admin_list_orders(status: str | None = None, db: Session = Depends(get_db)):
    q = select(Order).order_by(Order.id.desc())
    if status:
        q = q.where(Order.status == status)
    return db.scalars(q).all()


@router.patch("/bot/admin/orders/{order_id}/status", response_model=OrderOut, dependencies=[Depends(bot_admin_guard)])
def admin_set_status(order_id: int, payload: OrderStatusUpdate, db: Session = Depends(get_db)):
    if payload.status not in ("new", "in_progress", "closed", "rejected"):
        raise HTTPException(400, "Invalid status")

    o = db.get(Order, order_id)
    if not o:
        raise HTTPException(404, "Order not found")

    o.status = payload.status
    o.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(o)
    return o
