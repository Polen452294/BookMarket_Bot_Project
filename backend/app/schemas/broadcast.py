from datetime import datetime
from pydantic import BaseModel


class BroadcastCreate(BaseModel):
    text: str


class BroadcastOut(BaseModel):
    id: int
    text: str
    status: str
    created_at: datetime
    started_at: datetime | None = None
    finished_at: datetime | None = None

    class Config:
        from_attributes = True
