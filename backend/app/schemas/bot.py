from pydantic import BaseModel


class BotCreate(BaseModel):
    name: str
    token: str


class BotOut(BaseModel):
    id: int
    name: str
    is_active: bool

    class Config:
        from_attributes = True
