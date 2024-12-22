import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Enum, TIMESTAMP
from app.object.models import ActionType

from app.database import Base


class View(Base):
    __tablename__ = 'view'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    action_type: Mapped[ActionType] = mapped_column(Enum(ActionType))
    responsible: Mapped[str] = mapped_column(String)
    date: Mapped[str] = mapped_column(String)
    object_sum: Mapped[int] = mapped_column(Integer)
    commission_sum: Mapped[int] = mapped_column(Integer)
    agent_percent: Mapped[int] = mapped_column(Integer)
    crm_id: Mapped[str] = mapped_column(String)

    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                          default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                          default=lambda: datetime.datetime.now(datetime.timezone.utc),
                                                          onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))