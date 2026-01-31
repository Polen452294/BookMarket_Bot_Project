from sqlalchemy import Column, DateTime, Float, Integer, String, Text, Boolean, ForeignKey, func
from app.core.db import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    category_id = Column(ForeignKey("categories.id"))
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    description = Column(Text)

    price = Column(Integer, nullable=False)
    old_price = Column(Integer)
    cover_url = Column(String)

    year = Column(Integer)
    pages = Column(Integer)
    publisher = Column(String(255))
    language = Column(String(50))

    rating = Column(Float)
    reviews_count = Column(Integer, default=0)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

