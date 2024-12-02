from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.object.functions.land import create_land, get_land, get_lands
from app.object.schemas.land import LandCreate, LandResponse

router = APIRouter()


@router.post("/")
async def create_land_endpoint(land: LandCreate = Query(...),
                               media: List[UploadFile] = File(...),
                               db: AsyncSession = Depends(get_async_session)):
    return await create_land(db, land, media)


@router.get("/")
async def get_lands_endpoint(db: AsyncSession = Depends(get_async_session)):
    return await get_lands(db)


@router.get("/{land_id}", response_model=LandResponse)
async def get_land_endpoint(land_id: int, db: AsyncSession = Depends(get_async_session)):
    return await get_land(db, land_id)
