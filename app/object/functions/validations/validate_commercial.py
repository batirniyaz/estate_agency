from fastapi import HTTPException, status
from sqlalchemy.future import select

from app.district.model import District


async def validate_commercial(db, commercial):
    result = await db.execute(select(District).filter_by(name=commercial.district))
    district = result.scalars().first()
    if not district:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object district not found")

    if commercial.price <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object price must be greater than 0")
    elif not commercial.price.is_integer():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object price must be integer")

    if commercial.square_area <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object square_area must be greater than 0")
    elif not commercial.square_area.is_integer():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object square_area must be integer")

    if commercial.floor_number <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object floor_number must be greater than 0")
    elif not commercial.floor_number.is_integer():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object floor_number must be integer")

    if 0 >= commercial.agent_percent > 100:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object agent_percent must be greater than 0")
    elif not commercial.agent_percent.is_integer():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object agent_percent must be integer")

    return True
