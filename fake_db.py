import asyncio

from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession
import random

from app.database import get_async_session
from app.object.models.apartment import Apartment
from app.object.models.commercial import Commercial
from app.object.models.land import Land
from app.object.models import Category, ActionType, LocationLand, LocationCommercial, HouseType, HouseCondition, \
    CurrentStatus, BathroomType


fake = Faker()


districts = ['Yakkasaroy', 'Tashkent', 'Sergeli', 'Yashnabad']
metros = ['Sergeli', 'Olmazor', 'Chilanzar', 'Oybek']


async def create_fake_land(db: AsyncSession, count: int = 10):
    id_counter = 50
    for _ in range(count):
        land = Land(
            id=id_counter,
            district=random.choice(districts),
            title=fake.text(max_nb_chars=50),
            category=Category.LAND,
            action_type=random.choice(list(ActionType)),
            description=fake.text(),
            comment=fake.text(),
            price=fake.random_int(1000, 100000),
            rooms=fake.random_int(1, 10),
            square_area=fake.random_int(100, 500),
            live_square_area=fake.random_int(10, 100),
            floor_number=fake.random_int(1, 10),
            location=random.choice(list(LocationLand)),
            furnished=fake.boolean(),
            house_condition=random.choice(list(HouseCondition)),
            current_status=random.choice(list(CurrentStatus)),
            parking_place=fake.boolean(),
            agent_percent=fake.random_int(1, 10),
            agent_commission=fake.random_int(20, 200),
            crm_id=f'L_{id_counter}',
            responsible=random.choice(['Super Admin', 'batir']),
            media=[],
            created_at=fake.date_time_this_year(),
            updated_at=fake.date_time_this_year()
        )
        id_counter += 1
        db.add(land)
        print(f"Land created {land.title} and id: {land.id}")
    await db.commit()


async def create_fake_apartment(db: AsyncSession, count: int = 10):
    id_counter = 50
    for _ in range(count):
        apartment = Apartment(
            id=id_counter,
            district=random.choice(districts),
            metro_st=random.choice(metros),
            title=fake.text(max_nb_chars=50),
            category=Category.APARTMENT,
            action_type=random.choice(list(ActionType)),
            description=fake.text(),
            comment=fake.text(),
            price=fake.random_int(1000, 100000),
            house_type=random.choice(list(HouseType)),
            rooms=fake.random_int(1, 10),
            square_area=fake.random_int(10, 100),
            floor_number=fake.random_int(1, 20),
            floor=fake.random_int(0, 20),
            bathroom=random.choice(list(BathroomType)),
            furnished=fake.boolean(),
            house_condition=random.choice(list(HouseCondition)),
            current_status=random.choice(list(CurrentStatus)),
            name=fake.name(),
            phone_number='+998' + str(fake.random_int(900000000, 999999999)),
            agent_percent=fake.random_int(1, 15),
            agent_commission=fake.random_int(20, 200),
            crm_id=f'A_{id_counter}',
            responsible=random.choice(['Super Admin', 'batir']),
            media=[],
            created_at=fake.date_time_this_year(),
            updated_at=fake.date_time_this_year()
        )
        id_counter += 1
        db.add(apartment)
        print(f"Land created {apartment.title} and id: {apartment.id}")
    await db.commit()


async def create_fake_commercial(db: AsyncSession, count: int = 10):
    id_counter = 50
    for _ in range(count):
        commercial = Commercial(
            id=id_counter,
            district=random.choice(districts),
            title=fake.text(max_nb_chars=50),
            category=Category.COMMERCIAL,
            action_type=random.choice(list(ActionType)),
            description=fake.text(),
            comment=fake.text(),
            price=fake.random_int(1000, 100000),
            rooms=fake.random_int(1, 10),
            square_area=fake.random_int(100, 500),
            floor_number=fake.random_int(1, 10),
            location=random.choice(list(LocationCommercial)),
            furnished=fake.boolean(),
            house_condition=random.choice(list(HouseCondition)),
            current_status=random.choice(list(CurrentStatus)),
            parking_place=fake.boolean(),
            agent_percent=fake.random_int(1, 10),
            agent_commission=fake.random_int(20, 200),
            crm_id=f'C_{id_counter}',
            responsible=random.choice(['Super Admin', 'batir']),
            media=[],
            created_at=fake.date_time_this_year(),
            updated_at=fake.date_time_this_year()
        )
        id_counter += 1
        db.add(commercial)
        print(f"Land created {commercial.title} and id: {commercial.id}")
    await db.commit()


async def main():
    async for db in get_async_session():
        await create_fake_land(db, count=400)
        await create_fake_apartment(db, count=400)
        await create_fake_commercial(db, count=400)

if __name__ == "__main__":
    asyncio.run(main())
