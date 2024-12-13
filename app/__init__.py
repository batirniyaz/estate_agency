from fastapi import APIRouter
from app.metro.api import router as metro_router
from app.auth import router as auth_router
from app.district.api import router as district_router
from app.object.endpoints.apartment import router as apartment_router
from app.object.endpoints.land import router as land_router
from app.object.endpoints.commercial import router as commercial_router
from app.changes.endpoints import router as changes_router
from app.additional.api import router as additional_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(changes_router, prefix="/changes", tags=["Changes"])
router.include_router(metro_router, prefix="/metro", tags=["Metro"])
router.include_router(district_router, prefix="/district", tags=["District"])
router.include_router(apartment_router, prefix="/apartment", tags=["Apartment"])
router.include_router(land_router, prefix='/land', tags=["Land"])
router.include_router(commercial_router, prefix='/commercial', tags=["Commercial"])
router.include_router(additional_router, prefix='/additional', tags=["Additional"])

