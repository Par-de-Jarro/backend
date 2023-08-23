from fastapi import APIRouter

from .endpoints import todo

api_router = APIRouter()

api_router.include_router(todo.router, prefix="/todo", tags=["todo"])
