from fastapi import APIRouter
from app.metro.api import router as metro_router
from app.auth import router as auth_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(metro_router, prefix="/metro", tags=["Metro"])
