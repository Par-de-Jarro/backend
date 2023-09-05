from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, File, UploadFile

from app.api import deps
from app.common.exceptions import (
    AWSConfigException,
    AWSConfigExceptionHTTPException,
    RecordNotFoundException,
    RecordNotFoundHTTPException,
)
from app.user.schemas.user import UserCreate, UserSearchParams, UserUpdate, UserView
from app.user.services.user_service import UserService

router = APIRouter()


@router.post("/", response_model=UserView)
def create_user(user: UserCreate, service: UserService = Depends(deps.get_user_service)):
    return service.create(user)


@router.post(
    "/{id_user}/upload",
    response_model=UserView,
    dependencies=[Depends(deps.hass_access)],
)
def upload_profile_image(
    id_user: UUID,
    file: UploadFile = File(...),
    service: UserService = Depends(deps.get_user_service),
):
    try:
        return service.save_file(id_user=id_user, uploaded_file=file)
    except RecordNotFoundException:
        raise RecordNotFoundHTTPException(detail="User not found")
    except AWSConfigException as e:
        raise AWSConfigExceptionHTTPException(detail=e.detail)


@router.get(
    "/",
    response_model=List[UserView],
    dependencies=[Depends(deps.hass_access)],
)
def get_all(
    filters: UserSearchParams = Depends(UserSearchParams.params()),
    service: UserService = Depends(deps.get_user_service),
):
    return service.get_all(params=filters)


@router.get(
    "/{id_user}",
    response_model=UserView,
    dependencies=[Depends(deps.hass_access)],
)
def get_by_id(id_user: UUID, service: UserService = Depends(deps.get_user_service)):
    return service.get_by_id(id_user=id_user)


@router.put("/{id_user}", response_model=UserView)
def update_user(
    id_user: UUID, update: UserUpdate, service: UserService = Depends(deps.get_user_service)
):
    return service.update(id_user=id_user, update=update)


@router.delete(
    "/{id_user}",
    dependencies=[Depends(deps.hass_access)],
)
def delete_user(id_user: UUID, service: UserService = Depends(deps.get_user_service)):
    try:
        service.delete(id_user=id_user)
    except Exception as e:
        raise e
