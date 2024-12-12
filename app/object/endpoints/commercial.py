from typing import List, Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schema import UserRead
from app.auth.utils import get_current_active_user
from app.database import get_async_session

from app.object.functions.commercial import (create_commercial, get_commercials, get_commercial, update_commercial,
                                             delete_commercial)
from app.object.schemas.commercial import CommercialResponse, CommercialCreate, CommercialUpdate


router = APIRouter()


@router.post("/")
async def create_commercial_endpoint(current_user: Annotated[UserRead, Depends(get_current_active_user)],
                                     db: Annotated[AsyncSession, Depends(get_async_session)],
                                     commercial: CommercialCreate = Query(...),
                                     media: Optional[List[UploadFile]] = File(None)):
    try:
        return await create_commercial(
            db=db, commercial=commercial, media=media if media else None, current_user=current_user)
    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/")
async def get_commercials_endpoint(
        current_user: Annotated[UserRead, Depends(get_current_active_user)],
        db: Annotated[AsyncSession, Depends(get_async_session)],
        limit: int = Query(10, ge=1),
        page: int = Query(1, ge=1),
):
    return await get_commercials(db, limit, page)


@router.get("/{commercial_id}", response_model=CommercialResponse)
async def get_commercial_endpoint(current_user: Annotated[UserRead, Depends(get_current_active_user)],
                                  db: Annotated[AsyncSession, Depends(get_async_session)],
                                  commercial_id: int):
    return await get_commercial(db, commercial_id)


@router.put("/{commercial_id}")
async def update_commercial_endpoint(current_user: Annotated[UserRead, Depends(get_current_active_user)],
                                     db: Annotated[AsyncSession, Depends(get_async_session)],
                                     commercial_id: int, commercial: CommercialUpdate = Query(...),):
    return await update_commercial(db, commercial_id, commercial, current_user.full_name)


@router.delete("/{commercial_id}")
async def delete_commercial_endpoint(current_user: Annotated[UserRead, Depends(get_current_active_user)],
                                     commercial_id: int, db: Annotated[AsyncSession, Depends(get_async_session)]):
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Only admin can delete objects')
    return await delete_commercial(db, commercial_id, current_user.full_name)

