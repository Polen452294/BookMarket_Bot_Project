from pydantic import BaseModel


class MediaOut(BaseModel):
    id: int
    product_id: int
    type: str
    url: str
    sort_order: int

    class Config:
        from_attributes = True
