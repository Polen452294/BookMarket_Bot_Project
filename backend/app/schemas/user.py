from datetime import datetime
from pydantic import BaseModel


class UserUpsert(BaseModel):
    tg_id: int
    username: str | None = None
    first_name: str | None = None
    phone: str | None = None
    source: str | None = None


class UserOut(BaseModel):
    id: int
    tg_id: int
    username: str | None = None
    first_name: str | None = None
    phone: str | None = None
    source: str | None = None
    is_blocked: bool
    created_at: datetime
    last_seen_at: datetime | None = None

    class Config:
        from_attributes = True
