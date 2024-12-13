from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schema import UserRead
from app.auth.utils import get_current_active_user
from app.database import get_async_session
from app.district.crud import create_district, get_districts, get_district, update_district, delete_district
from app.district.schema import DistrictResponse, DistrictCreate, DistrictUpdate

router = APIRouter()


@router.post("/", response_model=DistrictResponse)
async def create_district_endpoint(
        district: DistrictCreate,
        current_user: Annotated[UserRead, Depends(get_current_active_user)],
        db: AsyncSession = Depends(get_async_session),
):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to create districts")
    return await create_district(db, district)


@router.get("/", response_model=list[DistrictResponse])
async def get_districts_endpoint(
        current_user: Annotated[UserRead, Depends(get_current_active_user)],
        db: AsyncSession = Depends(get_async_session)
):
    return await get_districts(db)


@router.get("/{district_id}", response_model=DistrictResponse)
async def get_district_endpoint(
        district_id: int,
        current_user: Annotated[UserRead, Depends(get_current_active_user)],
        db: AsyncSession = Depends(get_async_session)
):
    return await get_district(db, district_id)


@router.put("/{district_id}", response_model=DistrictResponse)
async def update_district_endpoint(
        district_id: int,
        district: DistrictUpdate,
        current_user: Annotated[UserRead, Depends(get_current_active_user)],
        db: AsyncSession = Depends(get_async_session)
):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to update districts")
    return await update_district(db, district_id, district)


@router.delete("/{district_id}")
async def delete_district_endpoint(
        district_id: int,
        current_user: Annotated[UserRead, Depends(get_current_active_user)],
        db: AsyncSession = Depends(get_async_session)
):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to delete districts")
    return await delete_district(db, district_id)
