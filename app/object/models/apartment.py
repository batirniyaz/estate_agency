import datetime

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, String, TIMESTAMP, Boolean, Enum, ForeignKey, Float

from app.database import Base

from app.object.models import Category, ActionType, HouseType, BathroomType, HouseCondition, CurrentStatus


class ApartmentMedia(Base):
    __tablename__ = 'apartment_media'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    url: Mapped[str] = mapped_column(String)
    media_type: Mapped[str] = mapped_column(String, nullable=True)
    apartment_id: Mapped[int] = mapped_column(Integer, ForeignKey('apartment.id'))

    apartment: Mapped['Apartment'] = relationship(back_populates='media', lazy='selectin')

    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                          default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                          default=lambda: datetime.datetime.now(datetime.timezone.utc),
                                                          onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))


class Apartment(Base):
    __tablename__ = 'apartment'

    # ID of the apartment
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    crm_id: Mapped[str] = mapped_column(String(length=255), unique=True)

    # Location of the apartment
    district: Mapped[str] = mapped_column(String(length=255))
    metro_st: Mapped[str] = mapped_column(String(length=255))

    # Details of the apartment
    title: Mapped[str] = mapped_column(String(length=255))
    category: Mapped[Category] = mapped_column(Enum(Category), default=Category.APARTMENT)
    action_type: Mapped[ActionType] = mapped_column(Enum(ActionType))
    media: Mapped[list['ApartmentMedia']] = relationship(back_populates='apartment', lazy='selectin')
    description: Mapped[str] = mapped_column(String, nullable=True)
    comment: Mapped[str] = mapped_column(String, nullable=True)
    price: Mapped[int] = mapped_column(Integer)

    # Additional information
    house_type: Mapped[HouseType] = mapped_column(Enum(HouseType))
    rooms: Mapped[int] = mapped_column(Integer)
    square_area: Mapped[int] = mapped_column(Integer)
    floor_number: Mapped[int] = mapped_column(Integer)
    floor: Mapped[int] = mapped_column(Integer)
    bathroom: Mapped[BathroomType] = mapped_column(Enum(BathroomType))
    furnished: Mapped[bool] = mapped_column(Boolean)
    house_condition: Mapped[HouseCondition] = mapped_column(Enum(HouseCondition))
    current_status: Mapped[CurrentStatus] = mapped_column(Enum(CurrentStatus), nullable=True)

    # Contact information
    name: Mapped[str] = mapped_column(String(length=255))
    phone_number: Mapped[str] = mapped_column(String(length=13))

    # Agent
    responsible: Mapped[str] = mapped_column(String)
    agent_percent: Mapped[int] = mapped_column(Integer, nullable=True)
    agent_commission: Mapped[float] = mapped_column(Float, nullable=True)

    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                          default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                          default=lambda: datetime.datetime.now(datetime.timezone.utc),
                                                          onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))
