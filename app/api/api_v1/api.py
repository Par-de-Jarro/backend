from fastapi import APIRouter

from app.api.api_v1.endpoints import (
    google,
    session,
    spot,
    spot_bill,
    spot_entry_request,
    university,
    user,
)

api_router = APIRouter()

api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(spot.router, prefix="/spot", tags=["spot"])
api_router.include_router(session.router, prefix="/session", tags=["session"])
api_router.include_router(university.router, prefix="/university", tags=["university"])
api_router.include_router(google.router, prefix="/google", tags=["google"])
api_router.include_router(
    spot_entry_request.router, prefix="/spot_entry_request", tags=["spot_entry_request"]
)

api_router.include_router(spot_bill.router, prefix="/spot_bill", tags=["spot_bill"])
