from fastapi import APIRouter

from .endpoints import session, user

api_router = APIRouter()

api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(session.router, prefix="/session", tags=["session"])
