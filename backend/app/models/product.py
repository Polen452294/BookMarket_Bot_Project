from sqlalchemy import Column, Integer, String, Text
from app.core.db import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text)

    author = Column(String)
    price = Column(Integer) 
