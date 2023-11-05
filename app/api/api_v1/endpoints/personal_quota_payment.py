from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, File, Security, UploadFile

from app.api import deps
from app.common.exceptions import (
    AWSConfigException,
    AWSConfigExceptionHTTPException,
    RecordNotFoundException,
    RecordNotFoundHTTPException,
)
from app.payment.schemas.personal_quota_payment import (
    GeneratePersonalQuotaPaymentConfig,
    PersonalQuotaPaymentGetParams,
    PersonalQuotaPaymentView,
)
from app.payment.services.personal_quota_payment import PersonalQuotaPaymentService

router = APIRouter()
validate_token = deps.token_auth()


@router.post(
    "/{id_personal_quota_payment}/upload",
    dependencies=[Depends(deps.hass_access)],
    response_model=PersonalQuotaPaymentView,
)
def upload_personal_quota_payment_images(
    id_personal_quota_payment: UUID,
    files: List[UploadFile] = File(...),
    id_user: UUID = Depends(deps.get_id_user_by_auth_token),
    service: PersonalQuotaPaymentService = Depends(deps.get_personal_quota_payment_service),
):
    try:
        return service.save_multiple_files(
            id_personal_quota_payment=id_personal_quota_payment,
            id_user=id_user,
            uploaded_files=files,
        )
    except RecordNotFoundException:
        raise RecordNotFoundHTTPException(detail="Personal Quota Payment not found")
    except AWSConfigException as e:
        raise AWSConfigExceptionHTTPException(detail=e.detail)


@router.post(
    "{id_personal_quota_payment}/pay",
    response_model=PersonalQuotaPaymentView,
    dependencies=[Depends(deps.hass_access)],
)
def pay_personal_quota_payment(
    id_personal_quota_payment: UUID,
    id_user: UUID = Depends(deps.get_id_user_by_auth_token),
    service: PersonalQuotaPaymentService = Depends(deps.get_personal_quota_payment_service),
):
    return service.pay(id_personal_quota_payment=id_personal_quota_payment, id_user=id_user)


@router.post(
    "/generate_personal_quota_payemnt",
    response_model=List[PersonalQuotaPaymentView],
    dependencies=[Depends(deps.hass_access)],
)
def generate_personal_quota_payemnt(
    config: GeneratePersonalQuotaPaymentConfig,
    id_user: UUID = Depends(deps.get_id_user_by_auth_token),
    service: PersonalQuotaPaymentService = Depends(deps.get_personal_quota_payment_service),
):
    return service.generate_personal_quota_payment(config=config, id_user=id_user)


@router.get(
    "/", response_model=List[PersonalQuotaPaymentView], dependencies=[Security(validate_token)]
)
def get_personal_quota_payment(
    service: PersonalQuotaPaymentService = Depends(deps.get_personal_quota_payment_service),
    filters: PersonalQuotaPaymentGetParams = Depends(PersonalQuotaPaymentGetParams.params()),
):
    return service.get_all(filters=filters)
