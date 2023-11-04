from uuid import UUID

from fastapi import UploadFile
from pyparsing import List
from sqlalchemy.orm import Session

from app.common.exceptions import AuthExceptionHTTPException, RecordNotFoundException
from app.common.repositories.aws_repository import AWSRepository
from app.common.services.base import BaseService
from app.payment.repositories.spot_bill import SpotBillRepository
from app.payment.schemas.spot_bill import SpotBillCreate, SpotBillUpdate, SpotBillView
from app.spot.services.spot_service import SpotService


class SpotBillService(BaseService[SpotBillCreate, SpotBillUpdate, SpotBillView]):
    repository: SpotBillRepository
    spot_service: SpotService

    def __init__(self, db: Session):
        super().__init__(repository=SpotBillRepository, db=db)
        self.aws_repository = AWSRepository(base_path="spot_bill")
        self.spot_service = SpotService(db=db)
        self.db = db

    def _check_if_allowed(self, id_user: UUID, id_spot_bill: UUID):
        spot_bill = self.get_by_id(id_spot_bill=id_spot_bill)

        if not (spot_bill):
            raise RecordNotFoundException()

        spot = self.spot_service.get_by_id(id_spot=spot_bill.id_spot)
        if spot.owner.id_user != id_user:
            raise AuthExceptionHTTPException(detail="User not allowed")

    def update(self, id_user: UUID, id_spot_bill: UUID, update: SpotBillUpdate) -> SpotBillView:
        self._check_if_allowed(id_user=id_user, id_spot_bill=id_spot_bill)

        return super().update(update, id_spot_bill=id_spot_bill)

    def create(self, id_user: UUID, create: SpotBillCreate) -> SpotBillView:
        self.spot_service._check_if_allowed(id_user=id_user, id_spot=create.id_spot)

        return super().create(create)

    def save_multiple_files(
        self, id_spot_bill: UUID, id_user: UUID, uploaded_files: List[UploadFile]
    ) -> List[str]:
        self._check_if_allowed(id_user=id_user, id_spot_bill=id_spot_bill)
        spot_bill = self.get_by_id(id_spot_bill=id_spot_bill)

        if not (spot_bill):
            raise RecordNotFoundException()
        images = self.aws_repository.save_multiple_files(
            id_obj=id_spot_bill, uploaded_files=uploaded_files
        )

        spot_bill_update = SpotBillUpdate(images=images)

        return self.update(id_spot_bill=id_spot_bill, update=spot_bill_update)
