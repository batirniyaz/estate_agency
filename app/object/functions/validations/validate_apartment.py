from fastapi import HTTPException, status
from sqlalchemy.future import select

from app.district.model import District
from app.metro.model import Metro


async def validate_apartment(db, apartment):
    result = await db.execute(select(District).filter_by(name=apartment.district))
    district = result.scalars().first()
    if not district:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object district not found")

    result = await db.execute(select(Metro).filter_by(name=apartment.metro_st))
    metro = result.scalars().first()
    if not metro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object metro not found")

    if apartment.price <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object price must be greater than 0")

    if not apartment.price.is_integer():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object price must be integer")

    if apartment.rooms < 0 or apartment.rooms > 30:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object room must be greater or equal than 0 and less than 30")

    if not apartment.rooms.is_integer():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object room must be integer")

    if not apartment.floor.is_integer():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object floor must be integer")

    if apartment.floor > apartment.floor_number or apartment.floor < -2:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object floor must be less than floor_number or greater than -3")

    if apartment.floor_number <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object floor_number must be greater than 0")

    if len(apartment.phone_number) != 13:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object phone must be 13 characters")

    if not apartment.phone_number[1:].isdigit():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object phone must be integer")

    if not apartment.phone_number[0] == "+":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object phone must start with +")

    if 0 >= apartment.agent_percent > 100:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object agent_percent must be greater than 0")

    if not apartment.agent_percent.is_integer():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object agent_percent must be integer")

    return True
