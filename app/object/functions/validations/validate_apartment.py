from fastapi import HTTPException, status
from sqlalchemy.future import select

from app.district.model import District
from app.metro.model import Metro


async def validate_apartment(db, apartment):
    if apartment.district:
        result = await db.execute(select(District).filter_by(name=apartment.district))
        district = result.scalars().first()
        if not district:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Объект района не найден")

    if apartment.metro_st:
        result = await db.execute(select(Metro).filter_by(name=apartment.metro_st))
        metro = result.scalars().first()
        if not metro:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Объект метро не найден")

    if apartment.price:
        if apartment.price <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Цена должна быть больше 0")

        if not apartment.price.is_integer():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Цена должна быть целым числом")

    if apartment.rooms:
        if apartment.rooms < 0 or apartment.rooms > 99:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Номер комнат объекта должен быть больше или равен 0 и меньше 99")

        if not apartment.rooms.is_integer():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Номер комнат должен быть целым числом.")

    if apartment.floor:
        if not apartment.floor.is_integer():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Этаж объекта должен быть целым числом.")

    if apartment.floor_number and apartment.floor:
        if apartment.floor > apartment.floor_number or apartment.floor < -2:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Этаж объекта должен быть меньше Этажности или больше -3")

    if apartment.floor_number:
        if apartment.floor_number <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Этажность должна быть больше 0")

    if apartment.phone_number:
        if len(apartment.phone_number) != 13:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Номер телефона должен быть длиной 13 чисел")

        if not apartment.phone_number[1:].isdigit():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Номер телефона должен содержать только числа")

        if not apartment.phone_number[0] == "+":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Номер телефона должен начинаться с +")

    if apartment.agent_percent:
        # if not 0 >= apartment.agent_percent > 100:
        #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        #                         detail="Object agent_percent must be between 0 and 100")

        if not apartment.agent_percent.is_integer():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Процент агента должен быть целым числом")
