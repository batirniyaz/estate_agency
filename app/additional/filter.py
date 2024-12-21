from datetime import datetime
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.object.models.apartment import Apartment
from app.object.models.commercial import Commercial
from app.object.models.land import Land
from app.object.models import ActionType, HouseType, BathroomType, CurrentStatus, HouseCondition, LocationCommercial, \
    LocationLand


async def filter_objects(
        db: AsyncSession,
        table: Optional[str] = None,
        action_type: Optional[ActionType] = None,
        district: Optional[str] = None,
        metro_st: Optional[str] = None,
        furniture: Optional[bool] = None,
        bathroom: Optional[BathroomType] = None,
        price_min: Optional[int] = None,
        price_max: Optional[int] = None,
        room_min: Optional[int] = None,
        room_max: Optional[int] = None,
        area_min: Optional[int] = None,
        area_max: Optional[int] = None,
        floor_min: Optional[int] = None,
        floor_max: Optional[int] = None,
        date_min: Optional[str] = None,
        date_max: Optional[str] = None,
        current_status: Optional[CurrentStatus] = None,
        status_date_min: Optional[str] = None,
        status_date_max: Optional[str] = None,
        house_type: Optional[HouseType] = None,
        house_condition: Optional[HouseCondition] = None,
        location_commercial: Optional[LocationCommercial] = None,
        location_land: Optional[LocationLand] = None,
        parking_place: Optional[bool] = None,
        responsible: Optional[str] = None,
):
    table_mapping = {
        "land": Land,
        "apartment": Apartment,
        "commercial": Commercial
    }

    table_obj = table_mapping.get(table)
    if not table_obj:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid table name")

    try:
        if date_min:
            date_min = datetime.strptime(date_min, '%Y-%m-%d')
        if date_max:
            date_max = datetime.strptime(date_max, '%Y-%m-%d')
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid date format. Expected; YYYY-MM-DD")


    stmt = select(table_obj)

    if action_type:
        stmt = stmt.filter_by(action_type=action_type)

    if district:
        stmt = stmt.filter_by(district=district)

    if metro_st:
        stmt = stmt.filter_by(metro_st=metro_st)

    if furniture:
        stmt = stmt.filter_by(furnished=furniture)

    if bathroom:
        stmt = stmt.filter_by(bathroom=bathroom)

    if price_min is not None and price_max is not None:
        stmt = stmt.where(and_(table_obj.price >= price_min, table_obj.price <= price_max))
    elif price_min is not None:
        stmt = stmt.where(and_(table_obj.price >= price_min))
    elif price_max is not None:
        stmt = stmt.where(and_(table_obj.price <= price_max))

    if room_min is not None and room_max is not None:
        stmt = stmt.where(and_(table_obj.rooms >= room_min, table_obj.rooms <= room_max))
    elif room_min is not None:
        stmt = stmt.where(and_(table_obj.rooms >= room_min))
    elif room_max is not None:
        stmt = stmt.where(and_(table_obj.rooms <= room_max))

    if area_min is not None and area_max is not None:
        stmt = stmt.where(and_(table_obj.square_area >= area_min, table_obj.square_area <= area_max))
    elif area_min:
        stmt = stmt.where(and_(table_obj.square_area >= area_min))
    elif area_max:
        stmt = stmt.where(and_(table_obj.square_area <= area_max))

    if table == 'apartment':
        if floor_min is not None and floor_max is not None:
            stmt = stmt.where(and_(table_obj.floor >= floor_min, table_obj.floor <= floor_max))
        if floor_min:
            stmt = stmt.where(and_(table_obj.floor >= floor_min))
        if floor_max:
            stmt = stmt.where(and_(table_obj.floor <= floor_max))

    if date_min is not None and date_max is not None:
        stmt = stmt.where(and_(table_obj.created_at >= date_min, table_obj.created_at <= date_max))
    elif date_min is not None:
        stmt = stmt.where(and_(table_obj.created_at >= date_min))
    elif date_max is not None:
        stmt = stmt.where(and_(table_obj.created_at <= date_max))

    if current_status:
        stmt = stmt.filter_by(current_status=current_status)

    if house_type:
        if table == 'apartment':
            stmt = stmt.filter_by(house_type=house_type)

    if house_condition:
        stmt = stmt.filter_by(house_condition=house_condition)

    if location_commercial:
        if table == 'commercial':
            stmt = stmt.filter_by(location=location_commercial)

    if location_land:
        if table == 'land':
            stmt = stmt.filter_by(location=location_land)

    if status_date_min is not None and status_date_max is not None:
        stmt = stmt.where(and_(table_obj.status_date >= status_date_min, table_obj.status_date <= status_date_max))
    elif status_date_min is not None:
        stmt = stmt.where(and_(table_obj.status_date >= status_date_min))
    elif status_date_max is not None:
        stmt = stmt.where(and_(table_obj.status_date <= status_date_max))

    if parking_place:
        if table == 'commercial' or table == 'land':
            stmt = stmt.filter_by(parking_place=parking_place)

    if responsible:
        stmt = stmt.where(and_(table_obj.responsible == responsible))

    stmt = stmt.order_by(table_obj.id.desc())

    result = await db.execute(stmt)
    return result.scalars().all()
