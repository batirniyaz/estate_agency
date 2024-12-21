from fastapi import HTTPException, status
from sqlalchemy.future import select

from app.district.model import District


async def validate_commercial(db, commercial):
    if commercial.district:
        result = await db.execute(select(District).filter_by(name=commercial.district))
        district = result.scalars().first()
        if not district:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object district not found")

    if commercial.price:
        if commercial.price <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object price must be greater than 0")
        elif not commercial.price.is_integer():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object price must be integer")

    if commercial.square_area:
        if commercial.square_area <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object square_area must be greater than 0")
        elif not commercial.square_area.is_integer():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object square_area must be integer")

    if commercial.rooms:
        if commercial.rooms < 0 or commercial.rooms > 99:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object room must be greater or equal than 0 and less than 99")

        if not commercial.rooms.is_integer():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object room must be integer")

    if commercial.floor_number:
        if commercial.floor_number <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object floor_number must be greater than 0")
        elif not commercial.floor_number.is_integer():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object floor_number must be integer")

    if commercial.agent_percent:
        # if not 0 >= commercial.agent_percent > 100:
        #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object agent_percent must be between 0 and 100")
        if not commercial.agent_percent.is_integer():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object agent_percent must be integer")
