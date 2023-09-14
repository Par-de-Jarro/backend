from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from app.api import deps
from app.common.exceptions import RecordNotFoundException, RecordNotFoundHTTPException
from app.spot.schemas.spot import SpotCreate, SpotUpdate, SpotView
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
    "/{id_spot}",
    response_model=SpotView,
    dependencies=[Depends(deps.hass_access)],
)
def get_by_id(id_spot: UUID, service: SpotService = Depends(deps.get_spot_service)):
    try:
        return service.get_by_id(id_spot=id_spot)
    except RecordNotFoundException:
        raise RecordNotFoundHTTPException(detail="Spot not found")


@router.put("/{id_spot}", response_model=SpotView)
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
