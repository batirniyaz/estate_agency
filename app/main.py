from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.auth.superuser import create_superuser
from app.database import create_db_and_tables
from app import router


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


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)
app.mount("/storage", StaticFiles(directory="app/storage"), name="storage")

