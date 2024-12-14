import os
from typing import List

from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.object.models.apartment import ApartmentMedia
from app.object.models.commercial import CommercialMedia
from app.object.models.land import LandMedia


async def delete_media(db: AsyncSession, media: List[int], table: str):
    try:
        # table: str = "land" | "apartment" | "commercial"
        purpose_table = None
        if table.lower() == "land":
            purpose_table = LandMedia
        elif table.lower() == "apartment":
            purpose_table = ApartmentMedia
        elif table.lower() == "commercial":
            purpose_table = CommercialMedia
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid table name")
        for media_id in media:

            media_res = await db.execute(select(purpose_table).filter_by(id=media_id))
            media_obj = media_res.scalars().first()
            if not media_obj:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Media {media_id} not found")

            file_path = os.path.join("app/storage", table.lower(), os.path.basename(media_obj.url))
            if os.path.exists(file_path):
                os.remove(file_path)

            await db.delete(media_obj)

        await db.commit()
        return {"detail": "Media deleted"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def get_media_by_id(db: AsyncSession, table: str, media_id: int):

    purpose_table = None
    if table.lower() == "land":
        purpose_table = LandMedia
    elif table.lower() == "apartment":
        purpose_table = ApartmentMedia
    elif table.lower() == "commercial":
        purpose_table = CommercialMedia
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid table name")

    media_res = await db.execute(select(purpose_table).filter_by(id=media_id))
    media = media_res.scalars().first()
    if not media:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media not found")

    return media


async def get_media(db: AsyncSession, table: str, limit: int, page: int):

    purpose_table = None
    if table.lower() == "land":
        purpose_table = LandMedia
    elif table.lower() == "apartment":
        purpose_table = ApartmentMedia
    elif table.lower() == "commercial":
        purpose_table = CommercialMedia
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid table name")

    total_count = await db.scalar(select(func.count(purpose_table.id)))
    media_res = await db.execute(select(purpose_table).order_by(purpose_table.id.desc()).limit(limit).offset((page - 1) * limit))
    media = media_res.scalars().all()

    return {"data": media if media else [], "total_count": total_count}