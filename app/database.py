from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME
import logging

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    pass


engine = create_async_engine(DATABASE_URL, pool_size=10, max_overflow=5)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            logger.error(f'Session rollback due to error: {e}')
            raise e
        finally:
            await session.close()
