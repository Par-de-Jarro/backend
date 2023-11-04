from sqlalchemy.orm import Session

from app.common.repositories.base import BaseRepository
from app.payment.models.spot_bill import SpotBill


class SpotBillRepository(BaseRepository):
    def __init__(self, db: Session):
        super(SpotBillRepository, self).__init__(SpotBill.id_spot_bill, model_class=SpotBill, db=db)
