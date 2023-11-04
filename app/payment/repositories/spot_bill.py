from datetime import date
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.common.repositories.base import BaseFinder, BaseRepository
from app.payment.models.spot_bill import SpotBill
from app.spot.models.spot import Spot


class SpotBillFinder(BaseFinder[SpotBill]):
    def filtered_by_id_spot(self, id_spot: Optional[UUID]):
        if id_spot:
            return SpotBillFinder(self.base_query.filter(SpotBill.id_spot == id_spot))

        return self

    def filtered_by_id_owner(self, id_owner: Optional[UUID]):
        if id_owner:
            return SpotBillFinder(
                self.base_query.join(Spot, Spot.id_spot == SpotBill.id_spot).filter(
                    Spot.id_user == id_owner
                )
            )

        return self

    def filtered_by_period(self, reference_date_start: date, reference_date_end: date):
        if reference_date_start and reference_date_end:
            return SpotBillFinder(
                self.base_query.filter(
                    SpotBill.reference_date.between(reference_date_start, reference_date_end)
                )
            )

        return self


class SpotBillRepository(BaseRepository):
    finder: SpotBillFinder

    def __init__(self, db: Session):
        super(SpotBillRepository, self).__init__(
            SpotBill.id_spot_bill, model_class=SpotBill, db=db, finder=SpotBillFinder
        )
