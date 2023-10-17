from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, File, Security, UploadFile

from app.api import deps
from app.common.exceptions import (
    AWSConfigException,
    AWSConfigExceptionHTTPException,
    NotAvailableSpotVacanciesException,
    NotAvailableSpotVacanciesHTTPException,
    RecordNotFoundException,
    RecordNotFoundHTTPException,
    SpotEntryRequestAlreadyAccepted,
    SpotEntryRequestAlreadyAcceptedHTTPException,
    SpotEntryRequestAlreadyDenied,
    SpotEntryRequestAlreadyDeniedHTTPException,
)
from app.spot.schemas.spot import SpotCreate, SpotSearchParams, SpotUpdate, SpotView
from app.spot.schemas.spot_entry_request import SpotEntryView
from app.spot.services.spot_entry_service import SpotEntryService
from app.spot.services.spot_service import SpotService

router = APIRouter()
validate_token = deps.token_auth()


@router.post(
    "/",
    response_model=SpotView,
    dependencies=[Depends(deps.hass_access)],
)
def create_spot(
    spot: SpotCreate,
    id_user: UUID = Depends(deps.get_id_user_by_auth_token),
    service: SpotService = Depends(deps.get_spot_service),
):
    create = SpotCreate(**spot.dict(exclude={"id_user"}), id_user=id_user)
    return service.create(create=create)


@router.get("/", response_model=List[SpotView], dependencies=[Security(validate_token)])
def get_all(
    service: SpotService = Depends(deps.get_spot_service),
):
    return service.get_all()


@router.get("/search", response_model=List[SpotView], dependencies=[Security(validate_token)])
def search(
    filters: SpotSearchParams = Depends(SpotSearchParams.params()),
    service: SpotService = Depends(deps.get_spot_service),
):
    return service.search(filters)


@router.get("/{id_spot}", response_model=SpotView, dependencies=[Security(validate_token)])
def get_by_id(id_spot: UUID, service: SpotService = Depends(deps.get_spot_service)):
    try:
        return service.get_by_id(id_spot=id_spot)
    except RecordNotFoundException:
        raise RecordNotFoundHTTPException(detail="Spot not found")


@router.put("/{id_spot}", dependencies=[Depends(deps.hass_access)], response_model=SpotView)
def update_spot(
    id_spot: UUID,
    update: SpotUpdate,
    id_user: UUID = Depends(deps.get_id_user_by_auth_token),
    service: SpotService = Depends(deps.get_spot_service),
):
    try:
        return service.update(id_spot=id_spot, update=update, id_user=id_user)
    except RecordNotFoundException:
        raise RecordNotFoundHTTPException(detail="Spot not found")


@router.delete(
    "/{id_spot}",
    dependencies=[Depends(deps.hass_access)],
)
def delete_spot(
    id_spot: UUID,
    service: SpotService = Depends(deps.get_spot_service),
    id_user: UUID = Depends(deps.get_id_user_by_auth_token),
):
    try:
        service.delete(id_spot=id_spot, id_user=id_user)
    except RecordNotFoundException:
        raise RecordNotFoundHTTPException(detail="Spot not found")


@router.post("/{id_spot}/upload", dependencies=[Depends(deps.hass_access)], response_model=SpotView)
def upload_spot_images(
    id_spot: UUID,
    files: List[UploadFile] = File(...),
    id_user: UUID = Depends(deps.get_id_user_by_auth_token),
    service: SpotService = Depends(deps.get_spot_service),
):
    try:
        return service.save_multiple_files(id_spot=id_spot, id_user=id_user, uploaded_files=files)
    except RecordNotFoundException:
        raise RecordNotFoundHTTPException(detail="Spot not found")
    except AWSConfigException as e:
        raise AWSConfigExceptionHTTPException(detail=e.detail)


@router.post(
    "/{id_spot}/request", dependencies=[Depends(deps.hass_access)], response_model=SpotEntryView
)
def request_spot_entry(
    id_spot: UUID,
    service: SpotEntryService = Depends(deps.get_spot_entry_service),
    id_user: UUID = Depends(deps.get_id_user_by_auth_token),
):
    try:
        return service.request_entry(id_user, id_spot)
    except RecordNotFoundException:
        raise RecordNotFoundHTTPException(detail="Spot not found")
    except NotAvailableSpotVacanciesException:
        raise NotAvailableSpotVacanciesHTTPException()


@router.post(
    "/{id_spot_entry_request}/reject",
    dependencies=[Depends(deps.hass_access)],
    response_model=SpotEntryView,
)
def reject_spot_entry(
    id_spot_entry_request: UUID,
    service: SpotEntryService = Depends(deps.get_spot_entry_service),
    id_user: UUID = Depends(deps.get_id_user_by_auth_token),
):
    try:
        return service.reject_entry(id_spot_entry_request=id_spot_entry_request, id_user=id_user)
    except RecordNotFoundException:
        raise RecordNotFoundHTTPException(detail="Spot Entry Request not found")
    except SpotEntryRequestAlreadyAccepted:
        raise SpotEntryRequestAlreadyAcceptedHTTPException()
    except SpotEntryRequestAlreadyDenied:
        raise SpotEntryRequestAlreadyDeniedHTTPException()


@router.post(
    "/{id_spot_entry_request}/accept",
    dependencies=[Depends(deps.hass_access)],
    response_model=SpotEntryView,
)
def accept_spot_entry(
    id_spot_entry_request: UUID,
    service: SpotEntryService = Depends(deps.get_spot_entry_service),
    id_user: UUID = Depends(deps.get_id_user_by_auth_token),
):
    try:
        return service.accept_entry(id_spot_entry_request=id_spot_entry_request, id_user=id_user)
    except RecordNotFoundException:
        raise RecordNotFoundHTTPException(detail="Spot Entry Request not found")
    except SpotEntryRequestAlreadyAccepted:
        raise SpotEntryRequestAlreadyAcceptedHTTPException()
    except SpotEntryRequestAlreadyDenied:
        raise SpotEntryRequestAlreadyDeniedHTTPException()
    except NotAvailableSpotVacanciesException:
        raise NotAvailableSpotVacanciesHTTPException()
