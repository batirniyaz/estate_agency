from fastapi import HTTPException, status
from sqlalchemy.future import select

from app.district.model import District


async def validate_land(db, land):
    if land.district:
        result = await db.execute(select(District).filter_by(name=land.district))
        district = result.scalars().first()
        if not district:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Район объекта не найден")

    if land.price:
        if land.price <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Цена объекта должна быть больше 0")
        elif not land.price.is_integer():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Цена объекта должна быть целым числом")

    if land.square_area:
        if land.square_area <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Площадь объекта должна быть больше 0")
        elif not land.square_area.is_integer():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Площадь объекта должна быть целым числом")

    if land.live_square_area and land.square_area:
        if land.live_square_area <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Жилая площадь объекта должна быть больше 0")
        elif not land.live_square_area.is_integer():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Жилая площадь объекта должна быть целым числом")
        elif land.live_square_area > land.square_area:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Жилая площадь объекта не может быть больше общей площади")

    if land.floor_number:
        if land.floor_number <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Этажность объекта должна быть больше 0")
        elif not land.floor_number.is_integer():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Этажность объекта должна быть целым числом")

    if land.agent_percent:
        # if not 0 >= land.agent_percent > 100:
        #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object agent_percent must be between 0 and 100")
        if not land.agent_percent.is_integer():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Процент агента должен быть целым числом")
