from fastapi import APIRouter
from .api import router as auth_router, router_user as user_router

router = APIRouter()
router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(user_router, prefix="/user", tags=["User"])
