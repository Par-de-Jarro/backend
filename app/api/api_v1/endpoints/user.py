from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from app.api import deps
from app.user.schemas.user import UserCreate, UserUpdate, UserView
from app.user.services.user_service import UserService

router = APIRouter()


@router.post("/", response_model=UserView)
def create_user(user: UserCreate, service: UserService = Depends(deps.get_user_service)):
    return service.create(user)


@router.get(
    "/",
    response_model=List[UserView],
    dependencies=[Depends(deps.hass_access)],
)
def get_all(service: UserService = Depends(deps.get_user_service)):
    try:
        service.get_all()
    except Exception as e:
        raise e
    return service.get_all()


@router.get(
    "/{id_user}",
    response_model=List[UserView],
    dependencies=[Depends(deps.hass_access)],
)
def get_by_id(id_user: UUID, service: UserService = Depends(deps.get_user_service)):
    try:
        service.get_by_id(id_user=id_user)
    except Exception as e:
        raise e


@router.put("/", response_model=UserView)
def update_user(id: UUID, user: UserUpdate, service: UserService = Depends(deps.get_user_service)):
    try:
        service.update(id, user)
    except Exception as e:
        raise e


@router.delete(
    "/{id_user}",
    dependencies=[Depends(deps.hass_access)],
)
def delete_user(id: UUID, service: UserService = Depends(deps.get_user_service)):
    try:
        service.delete(id)
    except Exception as e:
        raise e
    return {"message": "User deleted successfully"}
