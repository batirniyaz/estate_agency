from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.object.functions.land import create_land, get_land
from app.object.schemas.land import LandCreate, LandResponse

router = APIRouter()


@router.post("/", response_model=LandResponse, status_code=status.HTTP_201_CREATED)
async def create_land_endpoint(land: LandCreate,
                               media: List[UploadFile] = File(...),
                               db: AsyncSession = Depends(get_async_session)):
    return await create_land(db, land, media)


@router.get("/{land_id}", response_model=LandResponse)
async def get_land_endpoint(land_id: int, db: AsyncSession = Depends(get_async_session)):
    return await get_land(db, land_id)
