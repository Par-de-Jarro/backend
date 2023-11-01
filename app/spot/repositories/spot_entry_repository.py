from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.common.repositories.base import BaseFinder, BaseRepository
from app.spot.models.spot import Spot
from app.spot.models.spot_entry_request import SpotEntryRequest


class SpotEntryRequestFinder(BaseFinder[SpotEntryRequest]):
    def filtered_by_id_user(self, id_user: Optional[UUID]):
        if id_user:
            return SpotEntryRequestFinder(
                self.base_query.filter(SpotEntryRequest.id_user == id_user)
            )

        return self

    def filtered_by_id_spot(self, id_spot: Optional[UUID]):
        if id_spot:
            return SpotEntryRequestFinder(
                self.base_query.filter(SpotEntryRequest.id_spot == id_spot)
            )

        return self

    def filtered_by_id_owner(self, id_owner: Optional[UUID]):
        if id_owner:
            return SpotEntryRequestFinder(
                self.base_query.join(Spot, Spot.id_spot == SpotEntryRequest.id_spot).filter(
                    Spot.id_user == id_owner
                )
            )

        return self


class SpotEntryRequestRepository(BaseRepository):
    finder: SpotEntryRequestFinder

    def __init__(self, db: Session):
        super(SpotEntryRequestRepository, self).__init__(
            SpotEntryRequest.id_spot_entry_request,
            model_class=SpotEntryRequest,
            db=db,
            finder=SpotEntryRequestFinder,
        )
