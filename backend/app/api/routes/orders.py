from __future__ import annotations

import json
from datetime import datetime, timezone, timedelta
from typing import Optional

from fastapi import Request
from fastapi import APIRouter, Depends, Header, HTTPException, Query, Response
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.config import settings
from app.core.db import get_db
from app.api.deps_bot_admin import bot_admin_guard

from app.models.order import Order
from app.models.user import User
from app.schemas.order import (
    OrderCreate,
    OrderOut,
    OrderStatusUpdate,
    OrderCommentUpdate,
    OrderNotifyInfo,
)

router = APIRouter(tags=["orders"])


# ---------------------------
# Helpers
# ---------------------------

ALLOWED_STATUSES = {"new", "in_progress", "closed", "rejected"}


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _require_web_admin_token(
    x_bot_admin_token: str | None,
    request: Request | None = None,
    ):
    if request and request.method == "OPTIONS":
        return

    if not x_bot_admin_token or x_bot_admin_token != settings.BOT_ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid bot admin token")


def _parse_json_param(value: str, default):
    try:
        return json.loads(value)
    except Exception:
        return default


def _apply_order_filters(q, flt: dict):
    # Минимально нужный фильтр для React Admin: status
    status = flt.get("status")
    if status:
        q = q.where(Order.status == status)
    return q


def _content_range(resource: str, start: int, end: int, total: int) -> str:
    # react-admin ожидает: "orders 0-9/123"
    if total <= 0:
        return f"{resource} 0-0/0"
    end = min(end, total - 1)
    start = min(start, end)
    return f"{resource} {start}-{end}/{total}"


# ---------------------------
# Bot endpoints
# ---------------------------

@router.post("/bot/orders", response_model=OrderOut)
def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.tg_id == payload.tg_id))
    if not user:
        raise HTTPException(404, "User not found (call /bot/users/upsert first)")

    # запрет второй заявки, если есть открытая
    open_order = db.scalar(
        select(Order).where(
            Order.user_id == user.id,
            Order.status.in_(["new", "in_progress"]),
        )
    )
    if open_order:
        raise HTTPException(409, "You already have an active order")

    now = _utcnow()
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
    return db.scalars(
        select(Order).where(Order.user_id == user.id).order_by(Order.id.desc())
    ).all()


@router.get("/bot/orders/{order_id}", response_model=OrderOut)
def get_order(order_id: int, tg_id: int, db: Session = Depends(get_db)):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(404, "Order not found")

    user = db.get(User, order.user_id)
    if not user or user.tg_id != tg_id:
        raise HTTPException(403, "Forbidden")

    return order


# ---------------------------
# Bot admin endpoints
# ---------------------------

@router.get(
    "/bot/admin/orders",
    response_model=list[OrderOut],
    dependencies=[Depends(bot_admin_guard)],
)
def admin_list_orders(status: str | None = None, db: Session = Depends(get_db)):
    q = select(Order).order_by(Order.id.desc())
    if status:
        q = q.where(Order.status == status)
    return db.scalars(q).all()


@router.patch(
    "/bot/admin/orders/{order_id}/status",
    response_model=OrderOut,
    dependencies=[Depends(bot_admin_guard)],
)
def admin_set_status(order_id: int, payload: OrderStatusUpdate, db: Session = Depends(get_db)):
    if payload.status not in ALLOWED_STATUSES:
        raise HTTPException(400, "Invalid status")

    o = db.get(Order, order_id)
    if not o:
        raise HTTPException(404, "Order not found")

    o.status = payload.status
    o.updated_at = _utcnow()
    db.commit()
    db.refresh(o)
    return o


@router.patch(
    "/bot/admin/orders/{order_id}/comment",
    response_model=OrderOut,
    dependencies=[Depends(bot_admin_guard)],
)
def set_comment(order_id: int, payload: OrderCommentUpdate, db: Session = Depends(get_db)):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(404, "Order not found")

    order.comment = (payload.comment or "").strip() or None
    order.updated_at = _utcnow()
    db.commit()
    db.refresh(order)
    return order


@router.get(
    "/bot/admin/orders/{order_id}/notify-info",
    response_model=OrderNotifyInfo,
    dependencies=[Depends(bot_admin_guard)],
)
def admin_notify_info(order_id: int, db: Session = Depends(get_db)):
    o = db.get(Order, order_id)
    if not o:
        raise HTTPException(404, "Order not found")

    u = db.get(User, o.user_id)
    if not u:
        raise HTTPException(404, "User not found")

    return OrderNotifyInfo(id=o.id, tg_id=u.tg_id, status=o.status)


@router.get("/bot/admin/stats", dependencies=[Depends(bot_admin_guard)])
def admin_stats(db: Session = Depends(get_db)):
    return {
        "orders": {
            "total": db.scalar(select(func.count()).select_from(Order)),
            "new": db.scalar(select(func.count()).select_from(Order).where(Order.status == "new")),
            "in_progress": db.scalar(select(func.count()).select_from(Order).where(Order.status == "in_progress")),
            "closed": db.scalar(select(func.count()).select_from(Order).where(Order.status == "closed")),
            "rejected": db.scalar(select(func.count()).select_from(Order).where(Order.status == "rejected")),
        },
        "users": {
            "total": db.scalar(select(func.count()).select_from(User)),
        },
    }


@router.delete("/bot/admin/orders/cleanup", dependencies=[Depends(bot_admin_guard)])
def cleanup_orders(
    status: str | None = None,
    older_than_days: int | None = None,
    db: Session = Depends(get_db),
):
    q = select(Order)

    if status:
        q = q.where(Order.status == status)

    if older_than_days:
        cutoff = _utcnow() - timedelta(days=older_than_days)
        q = q.where(Order.created_at < cutoff)

    orders = db.scalars(q).all()
    count = len(orders)

    for o in orders:
        db.delete(o)

    db.commit()
    return {"deleted": count}


# ---------------------------
# Web admin endpoints (React-Admin)
# ---------------------------

@router.get("/admin/orders", response_model=list[OrderOut])
def web_admin_orders(
    response: Response,
    range: str = Query(default='[0,9]'),
    sort: str = Query(default='["id","DESC"]'),
    filter: str = Query(default='{}'),
    x_bot_admin_token: Optional[str] = Header(default=None, alias="X-Bot-Admin-Token"),
    db: Session = Depends(get_db),
):
    """
    React-Admin LIST:
      GET /admin/orders?range=[0,9]&sort=["id","DESC"]&filter={}
    Must return:
      - JSON array
      - Content-Range header
    """
    #_require_web_admin_token(x_bot_admin_token)

    r0, r1 = _parse_json_param(range, [0, 9])
    sort_field, sort_dir = _parse_json_param(sort, ["id", "DESC"])
    flt = _parse_json_param(filter, {})

    r0 = int(r0)
    r1 = int(r1)
    limit = max(1, (r1 - r0) + 1)
    offset = max(0, r0)

    # base query
    q = select(Order)
    q = _apply_order_filters(q, flt)

    # total count for Content-Range
    # IMPORTANT: считаем по subquery, чтобы работало с where
    total = db.execute(select(func.count()).select_from(q.subquery())).scalar_one()

    # sorting
    col = getattr(Order, str(sort_field), None) or Order.id
    if str(sort_dir).upper() == "ASC":
        q = q.order_by(col.asc())
    else:
        q = q.order_by(col.desc())

    # pagination
    items = db.execute(q.offset(offset).limit(limit)).scalars().all()

    # Content-Range
    end = offset + len(items) - 1
    response.headers["Content-Range"] = _content_range("orders", offset, end, total)

    return items


@router.get("/admin/orders/{order_id}", response_model=OrderOut)
def web_admin_order(
    order_id: int,
    x_bot_admin_token: Optional[str] = Header(default=None, alias="X-Bot-Admin-Token"),
    db: Session = Depends(get_db),
):
    _require_web_admin_token(x_bot_admin_token)

    o = db.get(Order, order_id)
    if not o:
        raise HTTPException(404, "Order not found")
    return o


@router.patch("/admin/orders/{order_id}", response_model=OrderOut)
def web_admin_update_order(
    order_id: int,
    payload: dict,
    x_bot_admin_token: Optional[str] = Header(default=None, alias="X-Bot-Admin-Token"),
    db: Session = Depends(get_db),
):
    """
    React-Admin UPDATE:
      PATCH /admin/orders/{id}
      body: {"status":"in_progress"} or {"comment":"..."}
    """
    _require_web_admin_token(x_bot_admin_token)

    o = db.get(Order, order_id)
    if not o:
        raise HTTPException(404, "Order not found")

    if "status" in payload:
        st = payload.get("status")
        if st not in ALLOWED_STATUSES:
            raise HTTPException(400, "Invalid status")
        o.status = st

    if "comment" in payload:
        o.comment = (payload.get("comment") or "").strip() or None

    o.updated_at = _utcnow()
    db.commit()
    db.refresh(o)
    return o

@router.delete("/admin/orders/{order_id}")
def web_admin_delete_order(
    order_id: int,
    x_bot_admin_token: Optional[str] = Header(default=None, alias="X-Bot-Admin-Token"),
    db: Session = Depends(get_db),
):
    _require_web_admin_token(x_bot_admin_token)

    o = db.get(Order, order_id)
    if not o:
        raise HTTPException(404, "Order not found")

    try:
        db.delete(o)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Cannot delete order: it has related data (use status=closed/rejected instead)",
        )

    return {"id": order_id}

@router.options("/admin/orders")
def options_admin_orders():
    return Response(status_code=200)

@router.options("/admin/orders/{order_id}")
def options_admin_order(order_id: int):
    return Response(status_code=200)