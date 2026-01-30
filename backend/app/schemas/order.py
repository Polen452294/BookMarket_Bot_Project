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
    phone: str | None
    status: str
    comment: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    status: str

class OrderNotifyInfo(BaseModel):
    id: int
    tg_id: int
    status: str

class OrderCommentUpdate(BaseModel):
    comment: str