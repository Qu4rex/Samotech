from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, DeclarativeBase, declared_attr, mapped_column

from datetime import datetime


class Base(DeclarativeBase):
    """Базовый класс для всех моделей SQLAlchemy, предоставляющий общие атрибуты и методы."""
    
    __abstract__ = True

    @declared_attr.directive
    def  __tablename__(cls) -> str:
        return cls.__name__.lower()


class TimestampMixin:
    """ Миксин для добавления временных меток создания и обновления к моделям SQLAlchemy."""

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())