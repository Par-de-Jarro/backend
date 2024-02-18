from typing import List
from uuid import UUID

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.common.exceptions import AuthExceptionHTTPException, RecordNotFoundException, SpotHasNoOccupantsException
from app.common.repositories.aws_repository import AWSRepository
from app.common.services.base import BaseService
from app.payment.repositories.personal_quota_payment import PersonalQuotaPaymentRepository
from app.payment.schemas.personal_quota_payment import (
    GeneratePersonalQuotaPaymentConfig,
    PersonalQuotaPaymentCreate,
    PersonalQuotaPaymentGetParams,
    PersonalQuotaPaymentStatus,
    PersonalQuotaPaymentUpdate,
    PersonalQuotaPaymentView,
)
from app.payment.schemas.spot_bill import SpotBillGetParams
from app.payment.services.spot_bill import SpotBillService
from app.spot.services.spot_service import SpotService


class PersonalQuotaPaymentService(
    BaseService[PersonalQuotaPaymentCreate, PersonalQuotaPaymentUpdate, PersonalQuotaPaymentView]
):
    repository: PersonalQuotaPaymentRepository
    spot_bill_service: SpotBillService

    def __init__(self, db: Session):
        super().__init__(repository=PersonalQuotaPaymentRepository, db=db)
        self.aws_repository = AWSRepository(base_path="personal_quota_payment")
        self.spot_bill_service = SpotBillService(db=db)
        self.spot_service = SpotService(db=db)
        self.db = db

    def _check_if_allowed(self, id_user: UUID, id_personal_quota_payment: UUID):
        personal_quota_payment = self.get_by_id(id_personal_quota_payment=id_personal_quota_payment)
        owner = personal_quota_payment.spot_bill.spot.owner.id_user

        if not (personal_quota_payment):
            raise RecordNotFoundException()

        print(personal_quota_payment.id_user, owner)
        if personal_quota_payment.id_user != id_user and owner != id_user:
            raise AuthExceptionHTTPException(detail="User not allowed")

    def create(self, id_user: UUID, create: PersonalQuotaPaymentCreate) -> PersonalQuotaPaymentView:
        spot_bill = self.spot_bill_service.get_by_id(id_spot_bill=create.id_spot_bill)
        self.spot_service._check_if_allowed(id_user=id_user, id_spot=spot_bill.id_spot)

        return super().create(create)

    def save_multiple_files(
        self, id_personal_quota_payment: UUID, id_user: UUID, uploaded_files: List[UploadFile]
    ) -> PersonalQuotaPaymentView:
        self._check_if_allowed(id_user=id_user, id_personal_quota_payment=id_personal_quota_payment)
        personal_quota_payment = self.get_by_id(id_personal_quota_payment=id_personal_quota_payment)

        if not (personal_quota_payment):
            raise RecordNotFoundException()
        images = self.aws_repository.save_multiple_files(
            id_obj=id_personal_quota_payment, uploaded_files=uploaded_files
        )

        update = PersonalQuotaPaymentUpdate(images=images)

        return self.update(
            id_personal_quota_payment=id_personal_quota_payment, id_user=id_user, update=update
        )

    def update(
        self,
        id_user: UUID,
        id_personal_quota_payment: UUID,
        update: PersonalQuotaPaymentUpdate,
    ) -> PersonalQuotaPaymentView:
        self._check_if_allowed(id_user=id_user, id_personal_quota_payment=id_personal_quota_payment)
        return super().update(
            id_user=id_user, id_personal_quota_payment=id_personal_quota_payment, update=update
        )

    def pay(self, id_user: UUID, id_personal_quota_payment: UUID) -> PersonalQuotaPaymentView:
        update = PersonalQuotaPaymentUpdate(status=PersonalQuotaPaymentStatus.PAYED)

        return self.update(
            id_user=id_user, id_personal_quota_payment=id_personal_quota_payment, update=update
        )

    def generate_personal_quota_payment(
        self, id_user: UUID, config: GeneratePersonalQuotaPaymentConfig
    ) -> List[PersonalQuotaPaymentView]:
        self.spot_service._check_if_allowed(id_user=id_user, id_spot=config.id_spot)
        bills = self.spot_bill_service.get_all(
            filters=SpotBillGetParams(
                id_spot=config.id_spot,
                reference_date_start=config.reference_date_start,
                reference_date_end=config.reference_date_end,
            )
        )
        spot = self.spot_service.get_by_id(id_spot=config.id_spot)
        users = spot.users

        if len(users) < 1:
            raise SpotHasNoOccupantsException()

        created_quotas = []
        for bill in bills:
            divided_bill = bill.value / len(users)

            for user in users:
                create = PersonalQuotaPaymentCreate(
                    id_spot_bill=bill.id_spot_bill,
                    id_user=user.id_user,
                    value=divided_bill,
                    status=PersonalQuotaPaymentStatus.WAITING_FOR_PAYMENT,
                    images=[],
                    meta={"config": config.dict()},
                )

                quota = self.create(id_user=id_user, create=create)
                created_quotas.append(quota)

        return created_quotas

    def get_all(self, filters: PersonalQuotaPaymentGetParams) -> List[PersonalQuotaPaymentView]:
        finder = self.repository.finder

        return (
            finder.filtered_by_id_user(id_user=filters.id_user)
            .filtered_by_id_spot_bill(id_spot_bill=filters.id_spot_bill)
            .filtered_by_period(
                reference_date_start=filters.reference_date_start,
                reference_date_end=filters.reference_date_end,
            )
        ).all()
