from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from app.api import deps
from app.user.schemas.user import UserCreate, UserUpdate, UserUpdatePassWord, UserView
from app.user.services.user_service import UserService

router = APIRouter()


@router.post("/", response_model=UserView)
def create_user(user: UserCreate, service: UserService = Depends(deps.get_service)):
    return service.create(user)


@router.get(
    "/",
    response_model=List[UserView],
    dependencies=[Depends(deps.hass_access)],
)
def get_all_users(service: UserService = Depends(deps.get_user_service)):
    try:
        service.get_all()
    except Exception as e:
        raise e
    return service.get_all()


@router.get(
    "/",
    response_model=List[UserView],
    dependencies=[Depends(deps.hass_access)],
)
def get_user_by_id(id: UUID, service: UserService = Depends(deps.get_user_service)):
    try:
        service.get_by_id(id)
    except Exception as e:
        raise e
    return service.get_by_id(id)


@router.get(
    "/",
    response_model=List[UserView],
    dependencies=[Depends(deps.hass_access)],
)
def get_user_by_email(email: str, service: UserService = Depends(deps.get_user_service)):
    try:
        service.get_user_by_email(email)
    except Exception as e:
        raise e
    return service.get_user_by_email(email)


@router.get(
    "/",
    response_model=List[UserView],
    dependencies=[Depends(deps.hass_access)],
)
def get_user_by_document_id(
    document_id: str, service: UserService = Depends(deps.get_user_service)
):
    try:
        service.get_user_by_document_id(document_id)
    except Exception as e:
        raise e
    return service.get_user_by_document_id(document_id)


@router.get(
    "/",
    response_model=List[UserView],
    dependencies=[Depends(deps.hass_access)],
)
def get_user_by_cellphone(cellphone: str, service: UserService = Depends(deps.get_user_service)):
    try:
        service.get_user_by_cellphone(cellphone)
    except Exception as e:
        raise e
    return service.get_user_by_cellphone(cellphone)


@router.put("/", response_model=UserView)
def update_user(id: UUID, user: UserUpdate, service: UserService = Depends(deps.get_user_service)):
    try:
        service.update(id, user)
    except Exception as e:
        raise e
    return service.update(id, user)


@router.put("/", response_model=UserView)
def update_password(
    id: UUID, user: UserUpdatePassWord, service: UserService = Depends(deps.get_user_service)
):
    return service.update_password(id, user)


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
