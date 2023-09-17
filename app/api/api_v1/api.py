from fastapi import APIRouter

from .endpoints import session, spot, university, user

api_router = APIRouter()

api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(spot.router, prefix="/spot", tags=["spot"])
api_router.include_router(session.router, prefix="/session", tags=["session"])
api_router.include_router(university.router, prefix="/university", tags=["university"])
