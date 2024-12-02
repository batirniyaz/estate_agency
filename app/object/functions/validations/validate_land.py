from fastapi import HTTPException, status
from sqlalchemy.future import select

from app.district.model import District
from app.metro.model import Metro


async def validate_land(db, land):
    result = await db.execute(select(District).filter_by(name=land.district))
    district = result.scalars().first()
    if not district:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object district not found")

    result = await db.execute(select(Metro).filter_by(name=land.metro_st))
    metro = result.scalars().first()
    if not metro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object metro not found")

    if land.price <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object price must be greater than 0")
    elif not land.price.is_integer():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object price must be integer")

    if land.rooms <= 0 or land.rooms > 30:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object room must be greater than 0")
    elif not land.rooms.is_integer():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object room must be integer")

    if not land.floor.is_integer():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object floor must be integer")
    elif land.floor > land.floor_number:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object floor must be less than floor_number")

    if len(land.phone_number) != 13:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object phone must be 13 characters")
    elif not land.phone_number[1:].isdigit():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object phone must be integer")
    elif not land.phone_number[0] == "+":
        print(land.phone_number[1])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object phone must start with +")

    if 0 >= land.agent_percent > 100:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object agent_percent must be greater than 0")
    elif not land.agent_percent.is_integer():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object agent_percent must be integer")

    return True
