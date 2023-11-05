from datetime import date
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.common.repositories.base import BaseFinder, BaseRepository
from app.payment.models.personal_quota_payment import PersonalQuotaPayment
from app.payment.models.spot_bill import SpotBill


class PersonalQuotaPaymentFinder(BaseFinder[PersonalQuotaPayment]):
    def filtered_by_id_spot_bill(self, id_spot_bill: Optional[UUID]):
        if id_spot_bill:
            return PersonalQuotaPaymentFinder(
                self.base_query.filter(PersonalQuotaPayment.id_spot_bill == id_spot_bill)
            )

        return self

    def filtered_by_id_user(self, id_user: Optional[UUID]):
        if id_user:
            return PersonalQuotaPaymentFinder(
                self.base_query.filter(PersonalQuotaPayment.id_user == id_user)
            )

        return self

    def filtered_by_period(self, reference_date_start: date, reference_date_end: date):
        if reference_date_start and reference_date_end:
            return PersonalQuotaPaymentFinder(
                self.base_query.join(
                    PersonalQuotaPayment.id_spot_bill == SpotBill.id_spot_bill
                ).filter(SpotBill.reference_date.between(reference_date_start, reference_date_end))
            )

        return self


class PersonalQuotaPaymentRepository(BaseRepository):
    finder: PersonalQuotaPaymentFinder

    def __init__(self, db: Session):
        super(PersonalQuotaPaymentRepository, self).__init__(
            PersonalQuotaPayment.id_personal_quota_payment,
            model_class=PersonalQuotaPayment,
            db=db,
            finder=PersonalQuotaPaymentFinder,
        )
