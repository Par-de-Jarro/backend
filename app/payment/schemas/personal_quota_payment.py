from decimal import Decimal
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

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
    images: List[str]
    status: PersonalQuotaPaymentStatus


@omit("images", "id_personal_quota_payment")
class PersonalQuotaPaymentCreate(PersonalQuotaPayment):
    ...


class PersonalQuotaPaymentUpdate(BaseModel):
    value: Optional[Decimal]
    status: Optional[PersonalQuotaPaymentStatus]


@omit("university")
class SimplifiedUserView(UserView):
    ...


class PersonalQuotaPaymentView(PersonalQuotaPayment):
    user: SimplifiedUserView
    spot_bill: SpotBillView
