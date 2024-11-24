from fastapi import APIRouter
from .api import router as auth_router

router = APIRouter()
router.include_router(auth_router, prefix="/auth", tags=["auth"])
