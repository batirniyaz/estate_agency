import datetime

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, String, TIMESTAMP, Boolean, Enum, ForeignKey

from app.database import Base

from app.object.models import Category, ActionType, LocationCommercial, HouseCondition, CurrentStatus


class CommercialMedia(Base):
    __tablename__ = 'commercial_media'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    url: Mapped[str] = mapped_column(String)
    media_type: Mapped[str] = mapped_column(String, nullable=True)
    commercial_id: Mapped[int] = mapped_column(Integer, ForeignKey('commercial.id'))

    commercial: Mapped['Commercial'] = relationship(back_populates='media', lazy='selectin')

    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                          default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                          default=lambda: datetime.datetime.now(datetime.timezone.utc),
                                                          onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))


class Commercial(Base):
    __tablename__ = 'commercial'

    # ID of the land
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    crm_id: Mapped[str] = mapped_column(String(length=255), unique=True)

    # Location of the land
    district: Mapped[str] = mapped_column(String(length=255))

    # Details of the land
    title: Mapped[str] = mapped_column(String(length=50))
    category: Mapped[Category] = mapped_column(Enum(Category), default=Category.COMMERCIAL)
    action_type: Mapped[ActionType] = mapped_column(Enum(ActionType))
    media: Mapped[list['CommercialMedia']] = relationship(back_populates='commercial', lazy='selectin')
    description: Mapped[str] = mapped_column(String(length=6000), nullable=True)
    comment: Mapped[str] = mapped_column(String(length=6000), nullable=True)
    price: Mapped[int] = mapped_column(Integer)

    # Additional information
    rooms: Mapped[int] = mapped_column(Integer)
    square_area: Mapped[int] = mapped_column(Integer)
    floor_number: Mapped[int] = mapped_column(Integer)
    floor: Mapped[int] = mapped_column(Integer)
    location: Mapped[LocationCommercial] = mapped_column(Enum(LocationCommercial))
    furnished: Mapped[bool] = mapped_column(Boolean)
    house_condition: Mapped[HouseCondition] = mapped_column(Enum(HouseCondition))
    current_status: Mapped[CurrentStatus] = mapped_column(Enum(CurrentStatus))
    parking_place: Mapped[bool] = mapped_column(Boolean)

    # Agent
    responsible: Mapped[str] = mapped_column(String)
    agent_percent: Mapped[int] = mapped_column(Integer, nullable=True)
    agent_commission: Mapped[int] = mapped_column(Integer, nullable=True)

    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                          default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                          default=lambda: datetime.datetime.now(datetime.timezone.utc),
                                                          onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))


