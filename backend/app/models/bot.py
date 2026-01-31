from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class Bot(Base):
    __tablename__ = "bots"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)

    token: Mapped[str] = mapped_column(String(256), nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
