import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Enum, TIMESTAMP
from app.object.models import ActionType

from app.database import Base


class Deal(Base):
    __tablename__ = 'deal'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    action_type: Mapped[ActionType] = mapped_column(Enum(ActionType))
    responsible: Mapped[str] = mapped_column(String)
    date: Mapped[str] = mapped_column(String(10))
    crm_id: Mapped[str] = mapped_column(String)
    object_price: Mapped[int] = mapped_column(Integer)
    commission: Mapped[float] = mapped_column(Integer)
    agent_percent: Mapped[int] = mapped_column(Integer)

    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                          default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                          default=lambda: datetime.datetime.now(datetime.timezone.utc),
                                                          onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))

