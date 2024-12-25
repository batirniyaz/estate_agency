import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Enum, TIMESTAMP, Boolean, Float
from app.object.models import ActionType

from app.database import Base


class View(Base):
    __tablename__ = 'view'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    action_type: Mapped[ActionType] = mapped_column(Enum(ActionType))
    responsible: Mapped[str] = mapped_column(String)
    date: Mapped[str] = mapped_column(String(10))
    time: Mapped[str] = mapped_column(String(5))
    district: Mapped[str] = mapped_column(String, nullable=True)
    price: Mapped[int] = mapped_column(Integer)
    commission: Mapped[float] = mapped_column(Float)
    agent_percent: Mapped[int] = mapped_column(Integer)
    status_deal: Mapped[bool] = mapped_column(Boolean, default=False)
    crm_id: Mapped[str] = mapped_column(String)
    client_number: Mapped[str] = mapped_column(String(13), nullable=True)
    owner_number: Mapped[str] = mapped_column(String(13), nullable=True)

    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                          default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                          default=lambda: datetime.datetime.now(datetime.timezone.utc),
                                                          onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))