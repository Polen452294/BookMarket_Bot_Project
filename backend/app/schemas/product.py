from pydantic import BaseModel


class ProductCreate(BaseModel):
    title: str
    description: str | None = None


class ProductUpdate(BaseModel):
    title: str | None = None
    description: str | None = None


class ProductOut(BaseModel):
    id: int
    title: str
    description: str
    author: str | None
    price: int | None

    class Config:
        from_attributes = True


    class Config:
        from_attributes = True
