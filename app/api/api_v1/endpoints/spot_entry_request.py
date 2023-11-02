from uuid import UUID

from fastapi import APIRouter, Depends

from app.api import deps
from app.common.exceptions import (
    NotAvailableSpotVacanciesException,
    NotAvailableSpotVacanciesHTTPException,
    RecordNotFoundException,
    RecordNotFoundHTTPException,
    SpotEntryRequestAlreadyAccepted,
    SpotEntryRequestAlreadyAcceptedHTTPException,
    SpotEntryRequestAlreadyDenied,
    SpotEntryRequestAlreadyDeniedHTTPException,
)
from app.spot.schemas.spot_entry_request import SpotEntryRequestGetParams, SpotEntryView
from app.spot.services.spot_entry_service import SpotEntryService

router = APIRouter()
validate_token = deps.token_auth()

router = APIRouter()
validate_token = deps.token_auth()


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


@router.get(
    "/",
    dependencies=[Depends(deps.hass_access)],
)
def get_spot_entry_request(
    service: SpotEntryService = Depends(deps.get_spot_entry_service),
    filters: SpotEntryRequestGetParams = Depends(SpotEntryRequestGetParams.params()),
):
    return service.get_all(filters=filters)
