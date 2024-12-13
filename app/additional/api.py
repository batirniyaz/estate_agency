from typing import List

from fastapi import HTTPException, status, Depends, APIRouter, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.additional.delete_media import delete_media
from app.auth.schema import UserRead
from app.auth.utils import get_current_active_user
from app.database import get_async_session
from app.additional.search import search

router = APIRouter()


@router.get("/search/")
async def search_endpoint(
        current_user: UserRead = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_async_session),
        text: str = Query(..., title="Search text", description="Text to search")
):
    return await search(db, text)


@router.delete("/delete_media/")
async def delete_media_endpoint(
        current_user: UserRead = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_async_session),
        media: List[int] = Query(..., title="Media ids", description="List of media ids to delete"),
        table: str = Query(..., title="Table name", description="Table name to delete media from",
                           examples=["land", "apartment", "commercial"])
):
    return await delete_media(db, media, table)
