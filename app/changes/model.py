import datetime

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, String, TIMESTAMP, ForeignKey, Enum, JSON
from enum import Enum as enum
from typing import TYPE_CHECKING

from app.database import Base

if TYPE_CHECKING:
    from app.auth.model import User


class OperationType(enum):
    CREATE = 'CREATE'
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'


class ChangeLog(Base):
    __tablename__ = 'change_log'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    table_name: Mapped[str] = mapped_column(String(255))
    operation: Mapped[OperationType] = mapped_column(Enum(OperationType), nullable=False)
    before_data: Mapped[dict] = mapped_column(JSON, default={}, nullable=True)
    after_data: Mapped[dict] = mapped_column(JSON, default={}, nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=True)
    user: Mapped['User'] = relationship(back_populates='change_logs', lazy='selectin')

    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                          default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                          default=lambda: datetime.datetime.now(datetime.timezone.utc),
                                                          onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))
