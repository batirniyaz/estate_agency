from app.auth.model import User
from app.auth.utils import get_password_hash
from app.database import async_session_maker
from sqlalchemy.future import select


async def create_superuser():

    async with async_session_maker() as session:
        async with session.begin():
            result = await session.execute(select(User).filter_by(is_superuser=True))
            superuser = result.scalars().first()

            if not superuser:
                superuser = User(
                    phone="+998999999999",
                    email="admin@example.com",
                    full_name="Super User",
                    hashed_password=get_password_hash("admin"),
                    is_superuser=True,
                    disabled=False
                )
                session.add(superuser)
                await session.commit()
