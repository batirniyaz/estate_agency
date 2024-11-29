import datetime

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, String, TIMESTAMP, Boolean, Enum, ForeignKey

from app.database import Base

from app.object.models import Category, ActionType, HouseType, BathroomType, HouseCondition


class LandImage(Base):
    __tablename__ = 'land_image'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    url: Mapped[str] = mapped_column(String)
    land_id: Mapped[int] = mapped_column(Integer, ForeignKey('land.id'))

    land: Mapped['Land'] = relationship('Land', back_populates='images', lazy='selectin')

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
    metro_st: Mapped[str] = mapped_column(String(length=255))

    # Details of the land
    title: Mapped[str] = mapped_column(String(length=255))
    category: Mapped[Category] = mapped_column(Enum(Category), default=Category.LAND)
    action_type: Mapped[ActionType] = mapped_column(Enum(ActionType))
    images: Mapped[list['LandImage']] = relationship('Image', back_populates='land', lazy='selectin')
    description: Mapped[str] = mapped_column(String)
    comment: Mapped[str] = mapped_column(String)
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

    # Contact information
    name: Mapped[str] = mapped_column(String(length=255))
    phone_number: Mapped[str] = mapped_column(String(length=13))

    # Agent
    responsible: Mapped[str] = mapped_column(String)
    agent_percent: Mapped[int] = mapped_column(Integer, nullable=True)

    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                          default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                          default=lambda: datetime.datetime.now(datetime.timezone.utc),
                                                          onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))
