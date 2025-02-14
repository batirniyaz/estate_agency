from typing import List

from fastapi import HTTPException, status, Depends, APIRouter, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.additional.media_crud import delete_media, get_media_by_id, get_media
from app.auth.schema import UserRead
from app.auth.utils import get_current_active_user
from app.database import get_async_session
from app.additional.search import search, get_all_object
from app.additional.filter import filter_objects
from app.object.models import ActionType, HouseType, BathroomType, CurrentStatus, HouseCondition, LocationCommercial, \
    LocationLand

router = APIRouter()


@router.get("/search/")
async def search_endpoint(
        current_user: UserRead = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_async_session),
        text: str = Query(..., title="Search text", description="Text to search"),
        table: str = Query(..., title="Table name", description="Table name to search",
                           examples=["land", "apartment", "commercial"])
):
    return await search(db, text, table)


@router.delete("/delete_media/")
async def delete_media_endpoint(
        current_user: UserRead = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_async_session),
        media: List[int] = Query(..., title="Media ids", description="List of media ids to delete"),
        table: str = Query(..., title="Table name", description="Table name to delete media from",
                           examples=["land", "apartment", "commercial"])
):
    return await delete_media(db, media, table)


@router.get("/get_media/")
async def get_media_endpoint(
        current_user: UserRead = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_async_session),
        table: str = Query(..., title="Table name", description="Table name to get media from",
                           examples=["land", "apartment", "commercial"]),
        media_id: int = Query(..., title="Media id", description="Media id to get")
):
    return await get_media_by_id(db, table, media_id)


@router.get("/get_media_list/")
async def get_media_list_endpoint(
        current_user: UserRead = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_async_session),
        table: str = Query(..., title="Table name", description="Table name to get media from",
                           examples=["land", "apartment", "commercial"]),
        limit: int = Query(10, title="Limit", description="Limit of media to get"),
        page: int = Query(1, title="Page", description="Page number")
):
    return await get_media(db, table, limit, page)


@router.get("/get_all_object/")
async def get_all_object_endpoint(
        current_user: UserRead = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_async_session),
):
    return await get_all_object(db)


@router.get("/filter/")
async def filter_objects_endpoint(
        # current_user: UserRead = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_async_session),
        table: str = Query(..., title="Table name", description="Table name to filter",
                           examples=["land", "apartment", "commercial"]),
        action_type: ActionType = Query(None, title="Action type", description="Action type. Each one"),
        district: str = Query(None, title="District", description="District name. Each one"),
        metro_st: str = Query(None, title="Metro station", description="Metro station name. Only apart"),
        furniture: bool = Query(None, title="Furniture", description="Furniture availability. Each one"),
        bathroom: BathroomType = Query(None, title="Bathroom", description="Bathroom type. Only apart"),
        price_min: int = Query(None, title="Min price", description="Min price. Each one"),
        price_max: int = Query(None, title="Max price", description="Max price. Each one"),
        room_min: int = Query(None, title="Min rooms", description="Min rooms. Each one"),
        room_max: int = Query(None, title="Max rooms", description="Max rooms. Each one"),
        area_min: int = Query(None, title="Min area", description="Min area. Each one"),
        area_max: int = Query(None, title="Max area", description="Max area. Each one"),
        floor_min: int = Query(None, title="Min floor", description="Min floor. Each one"),
        floor_max: int = Query(None, title="Max floor", description="Max floor. Each one"),
        date_min: str = Query(None, title="Min date", description="Min date. Each one"),
        date_max: str = Query(None, title="Max date", description="Max date. Each one"),
        current_status: CurrentStatus = Query(None, title="Current status", description="Current status. Each one"),
        status_date_min: str = Query(None, title="Min status date", description="Min status date. Each one"),
        status_date_max: str = Query(None, title="Max status date", description="Max status date. Each one"),
        house_type: HouseType = Query(None, title="House type", description="House type. Only apart"),
        house_condition: HouseCondition = Query(None, title="House condition", description="House condition. Each one"),
        location_commercial: LocationCommercial = Query(None, title="Commercial location", description="Commercial location. Only comm"),
        location_land: LocationLand = Query(None, title="Land location", description="Land location. Only land"),
        parking_place: bool = Query(None, title="Parking place", description="Parking place availability. Only comm and land"),
        responsible: str = Query(None, title="Responsible", description="Responsible name. Each one"),
        limit: int = Query(None, title="Limit", description="Limit of objects to get"),
        page: int = Query(None, title="Page", description="Page number")
):
    return await filter_objects(
        db=db, table=table,
        district=district if district else None,
        action_type=action_type if action_type else None,
        metro_st=metro_st if metro_st else None,
        furniture=furniture if furniture else None,
        bathroom=bathroom if bathroom else None,
        price_min=price_min if price_min else None,
        price_max=price_max if price_max else None,
        room_min=room_min if room_min else None,
        room_max=room_max if room_max else None,
        area_min=area_min if area_min else None,
        area_max=area_max if area_max else None,
        floor_min=floor_min if floor_min else None,
        floor_max=floor_max if floor_max else None,
        date_min=date_min if date_min else None,
        date_max=date_max if date_max else None,
        current_status=current_status if current_status else None,
        status_date_min=status_date_min if status_date_min else None,
        status_date_max=status_date_max if status_date_max else None,
        house_type=house_type if house_type else None,
        house_condition=house_condition if house_condition else None,
        location_commercial=location_commercial if location_commercial else None,
        location_land=location_land if location_land else None,
        parking_place=parking_place if parking_place else None,
        responsible=responsible if responsible else None,
        limit=limit if limit else None,
        page=page if page else None
    )
