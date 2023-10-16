from sqlalchemy.orm import Session

from app.common.repositories.base import BaseRepository
from app.spot.models.spot_entry_request import SpotEntryRequest


class SpotEntryRequestRepository(BaseRepository):
    def __init__(self, db: Session):
        super(SpotEntryRequest, self).__init__(
            SpotEntryRequest.id_spot_entry_request, model_class=SpotEntryRequest, db=db
        )
