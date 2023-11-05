from datetime import date
from decimal import Decimal
from enum import Enum
from typing import List, Optional
from uuid import UUID

from fastapi_qp import QueryParam
from pydantic import BaseModel, Field

from app.common.schemas import omit
from app.payment.schemas.spot_bill import SpotBillView
from app.user.schemas.user import UserView


class PersonalQuotaPaymentStatus(Enum):
    PAYED = "PAYED"
    WAITING_FOR_PAYMENT = "WAITING_FOR_PAYMENT"


class PersonalQuotaPayment(BaseModel):
    id_personal_quota_payment: UUID
    id_spot_bill: UUID
    id_user: UUID
    value: Decimal
    images: Optional[List[str]] = Field(default=[])
    status: PersonalQuotaPaymentStatus
    meta: dict


@omit("images", "id_personal_quota_payment")
class PersonalQuotaPaymentCreate(PersonalQuotaPayment):
    ...


class PersonalQuotaPaymentUpdate(BaseModel):
    value: Optional[Decimal]
    status: Optional[PersonalQuotaPaymentStatus]
    images: Optional[List[str]]


@omit("university")
class SimplifiedUserView(UserView):
    ...


@omit("spot")
class SimplifiedSpotBillView(SpotBillView):
    ...


class PersonalQuotaPaymentView(PersonalQuotaPayment):
    user: SimplifiedUserView
    spot_bill: SimplifiedSpotBillView

    class Config:
        orm_mode = True


class GeneratePersonalQuotaPaymentConfig(BaseModel):
    id_spot: UUID
    reference_date_start: date
    reference_date_end: date


class PersonalQuotaPaymentGetParams(BaseModel, QueryParam):
    id_user: Optional[UUID]
    id_spot_bill: Optional[UUID]
    reference_date_start: Optional[date]
    reference_date_end: Optional[date]
