from sqlalchemy.orm import Session

from app.common.repositories.base import BaseRepository
from app.payment.models.personal_quota_payment import PersonalQuotaPayment


class PersonalQuotaPaymentRepository(BaseRepository):
    def __init__(self, db: Session):
        super(PersonalQuotaPaymentRepository, self).__init__(
            PersonalQuotaPayment.id_personal_quota_payment, model_class=PersonalQuotaPayment, db=db
        )
