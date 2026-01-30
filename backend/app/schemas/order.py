from datetime import datetime
from pydantic import BaseModel


class OrderCreate(BaseModel):
    tg_id: int
    text: str
    phone: str | None = None


class OrderOut(BaseModel):
    id: int
    user_id: int
    text: str
    phone: str | None = None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    status: str  # new|in_progress|closed|rejected
