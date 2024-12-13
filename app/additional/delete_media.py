import os
from typing import List

from fastapi import HTTPException, status
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
            print(purpose_table)

            media_res = await db.execute(select(purpose_table).filter_by(id=media_id))
            media_obj = media_res.scalars().first()
            if not media_obj:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media not found")

            file_path = os.path.join("app/storage", table.lower(), os.path.basename(media_obj.url))
            if os.path.exists(file_path):
                os.remove(file_path)

            await db.delete(media_obj)

        await db.commit()
        return {"detail": "Media deleted"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
