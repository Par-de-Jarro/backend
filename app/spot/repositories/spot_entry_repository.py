from decimal import Decimal
from typing import Optional
from uuid import UUID

from sqlalchemy import Boolean, Integer, cast
from sqlalchemy.orm import Session

from app.common.repositories.base import BaseFinder, BaseRepository, haversine
from app.spot.models.spot import Spot
from app.spot.models.spot_entry_request import SpotEntryRequest
from app.spot.models.spot_user import SpotUser


class SpotEntryRequestRepository(BaseFinder[Spot]): # usa o finder mesmo?

    def check_spot_availability(self, id_spot: UUID):
        # TODO
        pass

    def accept_entry_request(self, id_spot_entry_request: UUID):
        # TODO
        pass

    def user_spot_association(self):
        # TODO
        pass

    def reject_entry_request(self, id_spot_entry_request: UUID):
        # TODO
        pass

