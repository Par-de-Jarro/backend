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
from app.payment.schemas.spot_bill import SpotBillCreate, SpotBillView
from app.payment.services.spot_bill import SpotBillService

router = APIRouter()
validate_token = deps.token_auth()


@router.post(
    "/",
    response_model=SpotBillView,
    dependencies=[Depends(deps.hass_access)],
)
def create_spot_bill(
    spot_bill: SpotBillCreate,
    id_user: UUID = Depends(deps.get_id_user_by_auth_token),
    service: SpotBillService = Depends(deps.get_spot_bill_service),
):
    try:
        return service.create(id_user=id_user, create=spot_bill)
    except RecordNotFoundException:
        raise RecordNotFoundHTTPException(detail="Spot not found")


@router.post(
    "/{id_spot_bill}/upload", dependencies=[Depends(deps.hass_access)], response_model=SpotBillView
)
def upload_spot_bill_images(
    id_spot_bill: UUID,
    files: List[UploadFile] = File(...),
    id_user: UUID = Depends(deps.get_id_user_by_auth_token),
    service: SpotBillService = Depends(deps.get_spot_bill_service),
):
    try:
        return service.save_multiple_files(
            id_spot_bill=id_spot_bill, id_user=id_user, uploaded_files=files
        )
    except RecordNotFoundException:
        raise RecordNotFoundHTTPException(detail="Spot Bill not found")
    except AWSConfigException as e:
        raise AWSConfigExceptionHTTPException(detail=e.detail)
