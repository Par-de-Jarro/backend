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
from app.spot.schemas.spot import SpotCreate, SpotSearchParams, SpotUpdate, SpotView
from app.spot.services.spot_service import SpotService

router = APIRouter()


@router.post(
    "/",
    response_model=SpotView,
    dependencies=[Depends(deps.hass_access)],
)
def create_spot(spot: SpotCreate, service: SpotService = Depends(deps.get_spot_service)):
    return service.create(spot)


@router.get(
    "/",
    response_model=List[SpotView],
)
def get_all(
    service: SpotService = Depends(deps.get_spot_service),
):
    return service.get_all()


@router.get(
    "/search",
    response_model=List[SpotView],
)
def searh(
    filters: SpotSearchParams = Depends(SpotSearchParams.params()),
    service: SpotService = Depends(deps.get_spot_service),
):
    return service.search(filters)


@router.get(
    "/{id_spot}",
    response_model=SpotView,
)
def get_by_id(id_spot: UUID, service: SpotService = Depends(deps.get_spot_service)):
    try:
        return service.get_by_id(id_spot=id_spot)
    except RecordNotFoundException:
        raise RecordNotFoundHTTPException(detail="Spot not found")


@router.put("/{id_spot}", dependencies=[Depends(deps.hass_access)], response_model=SpotView)
def update_spot(
    id_spot: UUID, update: SpotUpdate, service: SpotService = Depends(deps.get_spot_service)
):
    try:
        return service.update(id_spot=id_spot, update=update)
    except RecordNotFoundException:
        raise RecordNotFoundHTTPException(detail="User not found")


@router.delete(
    "/{id_spot}",
    dependencies=[Depends(deps.hass_access)],
)
def delete_spot(id_spot: UUID, service: SpotService = Depends(deps.get_spot_service)):
    try:
        service.delete(id_spot=id_spot)
    except RecordNotFoundException:
        raise RecordNotFoundHTTPException(detail="Spot not found")


@router.post(
    "/{id_spot}/upload",
    dependencies=[Depends(deps.hass_access)],
)
def upload_announcement_images(
    id_spot: UUID,
    files: List[UploadFile] = File(...),
    service: SpotService = Depends(deps.get_spot_service),
):
    try:
        return service.save_multiple_files(id_spot=id_spot, uploaded_files=files)
    except RecordNotFoundException:
        raise RecordNotFoundHTTPException(detail="Spot not found")
    except AWSConfigException as e:
        raise AWSConfigExceptionHTTPException(detail=e.detail)
