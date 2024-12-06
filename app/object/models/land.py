import datetime

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, String, TIMESTAMP, Boolean, Enum, ForeignKey, Float

from app.database import Base

from app.object.models import Category, ActionType, LocationLand, HouseCondition, CurrentStatus


class LandMedia(Base):
    __tablename__ = 'land_media'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    url: Mapped[str] = mapped_column(String)
    media_type: Mapped[str] = mapped_column(String, nullable=True)
    land_id: Mapped[int] = mapped_column(Integer, ForeignKey('land.id'))

    land: Mapped['Land'] = relationship(back_populates='media', lazy='selectin')

    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                          default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                          default=lambda: datetime.datetime.now(datetime.timezone.utc),
                                                          onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))


class Land(Base):
    __tablename__ = 'land'

    # ID of the land
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    crm_id: Mapped[str] = mapped_column(String(length=255), unique=True)

    # Location of the land
    district: Mapped[str] = mapped_column(String(length=255))

    # Details of the land
    title: Mapped[str] = mapped_column(String(length=50))
    category: Mapped[Category] = mapped_column(Enum(Category), default=Category.LAND)
    action_type: Mapped[ActionType] = mapped_column(Enum(ActionType))
    media: Mapped[list['LandMedia']] = relationship(back_populates='land', lazy='selectin')
    description: Mapped[str] = mapped_column(String(length=6000), nullable=True)
    comment: Mapped[str] = mapped_column(String(length=6000), nullable=True)
    price: Mapped[int] = mapped_column(Integer)

    # Additional information
    rooms: Mapped[int] = mapped_column(Integer)
    square_area: Mapped[int] = mapped_column(Integer)
    live_square_area: Mapped[int] = mapped_column(Integer)
    floor_number: Mapped[int] = mapped_column(Integer)
    location: Mapped[LocationLand] = mapped_column(Enum(LocationLand))
    furnished: Mapped[bool] = mapped_column(Boolean)
    house_condition: Mapped[HouseCondition] = mapped_column(Enum(HouseCondition))
    current_status: Mapped[CurrentStatus] = mapped_column(Enum(CurrentStatus), nullable=True)
    parking_place: Mapped[bool] = mapped_column(Boolean)

    # Agent
    responsible: Mapped[str] = mapped_column(String)
    agent_percent: Mapped[int] = mapped_column(Integer, nullable=True)
    agent_commission: Mapped[float] = mapped_column(Float, nullable=True)

    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                          default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                          default=lambda: datetime.datetime.now(datetime.timezone.utc),
                                                          onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))

