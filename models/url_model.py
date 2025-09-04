from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String, func, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class URLModel(Base):
    __tablename__ = "urls"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(nullable=False)
    shortCode: Mapped[str] = mapped_column(
        String(7), unique=True, nullable=False, index=True
    )
    createdAt: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updatedAt: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    accessCount: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("0")
    )
