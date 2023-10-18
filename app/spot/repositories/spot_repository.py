from decimal import Decimal
from typing import Optional
from uuid import UUID

from sqlalchemy import Boolean, Integer, cast, or_
from sqlalchemy.orm import Session

from app.common.repositories.base import BaseFinder, BaseRepository, haversine
from app.spot.models.spot import Spot
from app.spot.models.spot_user import SpotUser


class SpotFinder(BaseFinder[Spot]):
    def filter_by_bathrooms_quantity(self, bathrooms_quantity: Optional[int]):
        if bathrooms_quantity is not None and bathrooms_quantity != 0:
            return SpotFinder(
                self.base_query.filter(
                    cast(Spot.key["convenience"]["bathrooms_quantity"], Integer)
                    == bathrooms_quantity
                )
            )

        return self

    def filter_by_rooms_quantity(self, rooms_quantity: Optional[int]):
        if rooms_quantity is not None and rooms_quantity != 0:
            return SpotFinder(
                self.base_query.filter(
                    cast(Spot.key["convenience"]["rooms_quantity"], Integer) == rooms_quantity
                )
            )

        return self

    def filter_by_distance_range(
        self, distance_range: Optional[int], lat: Optional[Decimal], long: Optional[Decimal]
    ):
        if distance_range is not None:
            return SpotFinder(
                self.base_query.filter(haversine(Spot.lat, Spot.long, lat, long) <= distance_range)
            )

        return self

    def find_by_id_user(self, id_user: Optional[UUID] = None):
        if id_user:
            return SpotFinder(
                self.base_query.join(
                    SpotUser, SpotUser.id_spot == Spot.id_spot, isouter=True
                ).filter(
                    or_(Spot.id_user == id_user, SpotUser.id_user == id_user),
                )
            )

        return self

    def filter_by_value_min(self, value_min: Optional[int]):
        if value_min is not None:
            return SpotFinder(self.base_query.filter(Spot.value >= value_min))

        return self

    def filter_by_value_max(self, value_max: Optional[int]):
        if value_max is not None:
            return SpotFinder(self.base_query.filter(Spot.value <= value_max))

        return self

    def filter_by_allow_smoker(self, allow_smoker: Optional[bool]):
        if allow_smoker is not None:
            return SpotFinder(
                self.base_query.filter(
                    cast(Spot.key["allowance"]["allow_smoker"], Boolean).is_(allow_smoker)
                )
            )
        return self

    def filter_by_allow_pet(self, allow_pet: Optional[bool]):
        if allow_pet is not None:
            return SpotFinder(
                self.base_query.filter(
                    cast(Spot.key["allowance"]["allow_pet"], Boolean).is_(allow_pet)
                )
            )
        return self

    def filter_by_has_elevator(self, has_elevator: Optional[bool]):
        if has_elevator is not None:
            return SpotFinder(
                self.base_query.filter(
                    cast(Spot.key["convenience"]["has_elevator"], Boolean).is_(has_elevator)
                )
            )
        return self


class SpotRepository(BaseRepository):
    finder: SpotFinder

    def __init__(self, db: Session):
        super(SpotRepository, self).__init__(
            Spot.id_spot, model_class=Spot, db=db, finder=SpotFinder
        )
