from typing import List, Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Query, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schema import UserRead
from app.auth.utils import get_current_active_user
from app.database import get_async_session

from app.object.functions.land import create_land, get_lands, get_land, update_land, delete_land
from app.object.schemas.land import LandUpdate, LandCreate, LandResponse

router = APIRouter()


@router.post("/")
async def create_land_endpoint(current_user: Annotated[UserRead, Depends(get_current_active_user)],
                               db: Annotated[AsyncSession, Depends(get_async_session)],
                               background_tasks: BackgroundTasks,
                               land: LandCreate = Query(...),
                               media: Optional[List[UploadFile]] = File(None)):
    return await create_land(db=db, land=land, media=media if media else None,
                             current_user=current_user, background_tasks=background_tasks)


@router.get("/")
async def get_lands_endpoint(
        current_user: Annotated[UserRead, Depends(get_current_active_user)],
        db: Annotated[AsyncSession, Depends(get_async_session)],
        limit: int = Query(10, ge=1),
        page: int = Query(1, ge=1),
):
    return await get_lands(db, limit, page)


@router.get("/{land_id}", response_model=LandResponse)
async def get_land_endpoint(current_user: Annotated[UserRead, Depends(get_current_active_user)],
                            db: Annotated[AsyncSession, Depends(get_async_session)],
                            land_id: int):
    return await get_land(db, land_id)


@router.put("/{land_id}")
async def update_land_endpoint(current_user: Annotated[UserRead, Depends(get_current_active_user)],
                               db: Annotated[AsyncSession, Depends(get_async_session)],
                               land_id: int, land: LandUpdate = Query(...),
                               media: Optional[List[UploadFile]] = File(None)):
    return await update_land(db=db, land_id=land_id, land=land, user=current_user,
                             media=media if media else None)


@router.delete("/{land_id}")
async def delete_land_endpoint(current_user: Annotated[UserRead, Depends(get_current_active_user)],
                               land_id: int, db: Annotated[AsyncSession, Depends(get_async_session)]):
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Only admin can delete objects')
    return await delete_land(db, land_id)
