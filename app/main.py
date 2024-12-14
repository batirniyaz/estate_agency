import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.auth.superuser import create_superuser
from app.changes.funcs import process_log_queue
from app.changes.track_models import register_event_listeners
from app.database import create_db_and_tables
from app import router

from app.bot.run_bot import run_bot


@asynccontextmanager
async def lifespan(main_app: FastAPI):
    await create_db_and_tables()
    await create_superuser()

    register_event_listeners()
    log_queue_task = asyncio.create_task(process_log_queue())

    # bot_task = asyncio.create_task(run_bot())

    try:
        yield
    finally:
        # bot_task.cancel()
        log_queue_task.cancel()
        try:
            await log_queue_task
            # await bot_task
        except asyncio.CancelledError:
            pass


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

