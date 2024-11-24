from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.auth import router as auth_router
from app.auth.utils import create_superuser
from app.database import create_db_and_tables
# from app.api import router


@asynccontextmanager
async def lifespan(main_app: FastAPI):
    await create_db_and_tables()
    await create_superuser()

    yield

app = FastAPI(
    title="Estate Agency Mini CRM system",
    version="0.1",
    summary="This is a mini CRM system for estate agencies",
    lifespan=lifespan,
)

app.include_router(auth_router)
# app.include_router(router)

