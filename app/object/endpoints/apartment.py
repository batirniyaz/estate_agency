from codecs import backslashreplace_errors
from typing import List, Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Query, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schema import UserRead
from app.auth.utils import get_current_active_user
from app.database import get_async_session
from app.object.functions.apartment import create_apartment, get_apartments, get_apartment, update_apartment, delete_apartment
from app.object.schemas.apartment import ApartmentUpdate, ApartmentCreate, ApartmentResponse

router = APIRouter()


@router.post("/")
async def create_apartment_endpoint(current_user: Annotated[UserRead, Depends(get_current_active_user)],
                                    db: Annotated[AsyncSession, Depends(get_async_session)],
                                    background_tasks: BackgroundTasks,
                                    apartment: ApartmentCreate = Query(...),
                                    media: Optional[List[UploadFile]] = File(None),):
    return await create_apartment(
        db=db, apartment=apartment, media=media if media else None, current_user=current_user,
        background_tasks=background_tasks)


@router.get("/")
async def get_apartment_endpoint(
        current_user: Annotated[UserRead, Depends(get_current_active_user)],
        db: Annotated[AsyncSession, Depends(get_async_session)],
        limit: int = Query(10, ge=1),
        page: int = Query(1, ge=1),
):
    return await get_apartments(db, limit, page)


@router.get("/{apartment_id}", response_model=ApartmentResponse)
async def get_apartment_endpoint(current_user: Annotated[UserRead, Depends(get_current_active_user)],
                                 db: Annotated[AsyncSession, Depends(get_async_session)],
                                 apartment_id: int):
    return await get_apartment(db, apartment_id)


@router.put("/{apartment_id}")
async def update_apartment_endpoint(current_user: Annotated[UserRead, Depends(get_current_active_user)],
                                    db: Annotated[AsyncSession, Depends(get_async_session)],
                                    background_tasks: BackgroundTasks,
                                    apartment_id: int, apartment: ApartmentUpdate = Query(...),
                                    media: Optional[List[UploadFile]] = File(None)):
    return await update_apartment(
        db=db, apartment_id=apartment_id,
        apartment=apartment, user=current_user,
        media=media if media else None,
        background_tasks=background_tasks)


@router.delete("/{apartment_id}")
async def delete_apartment_endpoint(current_user: Annotated[UserRead, Depends(get_current_active_user)],
                                    apartment_id: int, db: Annotated[AsyncSession, Depends(get_async_session)]):
    if not current_user.is_superuser:
        HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Only admin can delete objects')
    return await delete_apartment(db, apartment_id)





