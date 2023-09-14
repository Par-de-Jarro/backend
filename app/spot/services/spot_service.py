from decimal import Decimal
from typing import List
from uuid import UUID

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.common.exceptions import RecordNotFoundException
from app.common.repositories.aws_repository import AWSRepository
from app.common.repositories.base import haversine
from app.common.services.base import BaseService
from app.spot.models.spot import Spot
from app.spot.repositories.spot_repository import SpotFinder, SpotRepository
from app.spot.schemas.spot import Images, SpotCreate, SpotSearchParams, SpotUpdate, SpotView
from app.user.models.user import User
from app.user.schemas.user import UserView


class SpotService(BaseService[SpotCreate, SpotUpdate, SpotView]):
    repository: SpotRepository
    db: Session

    def __init__(self, db: Session):
        super().__init__(repository=SpotRepository, db=db)
        self.aws_repository = AWSRepository(base_path="spot")
        self.db = db

    def search(self, filters: SpotSearchParams):
        finder = SpotFinder(base_query=self._get_base_query(lat=filters.lat, long=filters.long))

        result = (
            finder.filter_by_bathrooms_quantity_min(filters.bathrooms_quantity_min)
            .filter_by_bathrooms_quantity_max(filters.bathrooms_quantity_max)
            .filter_by_rooms_quantity_min(filters.rooms_quantity_min)
            .filter_by_rooms_quantity_max(filters.rooms_quantity_max)
            .filter_by_distance_range(
                distance_range=filters.distance_range, lat=filters.lat, long=filters.long
            )
            .filter_by_value_min(filters.value_min)
            .filter_by_value_max(filters.value_max)
            .filter_by_allow_smoker(filters.allow_smoker)
            .filter_by_allow_pet(filters.allow_pet)
            .filter_by_has_elevator(filters.has_elevator)
        )

        return [self._parse_result(item) for item in result.all()]

    def save_multiple_files(self, id_spot: UUID, uploaded_files: List[UploadFile]) -> List[str]:
        spot = self.get_by_id(id_spot=id_spot)
        if not (spot):
            raise RecordNotFoundException()

        images = self.aws_repository.save_multiple_files(
            id_obj=id_spot, uploaded_files=uploaded_files
        )

        images = [Images(image_order=index, image_url=image) for index, image in enumerate(images)]
        spot_update = SpotUpdate(images=images)

        return self.update(id_spot=id_spot, update=spot_update)

    def _parse_result(self, result) -> SpotView:
        return SpotView(**result, owner=UserView(**result["User"].__dict__))

    def _get_base_query(self, lat: Decimal, long: Decimal):
        return (
            self.db.query(
                Spot.__table__,
            )
            .add_column(
                haversine(Spot.lat, Spot.long, lat, long).label("distance"),
            )
            .add_entity(User)
            .filter(Spot.deleted_at.is_(None))
            .order_by("distance")
        )
