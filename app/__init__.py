from fastapi import APIRouter
from app.metro.api import router as metro_router
from app.auth import router as auth_router
from app.district.api import router as district_router
from app.object.endpoints.land import router as land_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(metro_router, prefix="/metro", tags=["Metro"])
router.include_router(district_router, prefix="/district", tags=["District"])
router.include_router(land_router, prefix="/land", tags=["Land"])
