from fastapi import APIRouter
from app.metro.api import router as metro_router
from app.auth import router as auth_router
from app.district.api import router as district_router
from app.object.endpoints.apartment import router as apartment_router
from app.object.endpoints.land import router as land_router
from app.object.endpoints.commercial import router as commercial_router
from app.changes.endpoints import router as changes_router
from app.additional.api import router as additional_router
from app.report.views.api import router as view_router
from app.report.clients.api import router as client_router
from app.report.deals.api import router as deal_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(changes_router, prefix="/changes", tags=["Changes"])
router.include_router(metro_router, prefix="/metro", tags=["Metro"])
router.include_router(district_router, prefix="/district", tags=["District"])
router.include_router(apartment_router, prefix="/apartment", tags=["Apartment"])
router.include_router(land_router, prefix='/land', tags=["Land"])
router.include_router(commercial_router, prefix='/commercial', tags=["Commercial"])
router.include_router(additional_router, prefix='/additional', tags=["Additional"])
router.include_router(view_router, prefix='/views', tags=["Views"])
router.include_router(client_router, prefix='/clients', tags=["Clients"])
router.include_router(deal_router, prefix='/deals', tags=["Deals"])

