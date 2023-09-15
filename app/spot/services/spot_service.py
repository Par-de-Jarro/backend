from decimal import Decimal
from typing import List
from uuid import UUID

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.common.exceptions import AuthExceptionHTTPException, RecordNotFoundException
from app.common.lib.google_address_api import GoogleAddressApi
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
    google_address_api: GoogleAddressApi

    def __init__(self, db: Session):
        super().__init__(repository=SpotRepository, db=db)
        self.aws_repository = AWSRepository(base_path="spot")
        self.google_address_api = GoogleAddressApi()
        self.db = db

    def create(self, create: SpotCreate) -> SpotView:
        if create.lat and create.long:
            return super().create(create)
        else:
            lat, long = self.google_address_api.get_location_coordinates(
                create.street, create.city, create.zip_code
            )

            spot_create = SpotCreate(**create.dict(exclude={"lat", "long"}), lat=lat, long=long)
            return super().create(spot_create)

    def update(self, id_user: UUID, id_spot: UUID, update: SpotUpdate) -> SpotView:
        self._check_if_allowed(id_user=id_user, id_spot=id_spot)

        return super().update(update=update, id_spot=id_spot)

    def delete(self, id_user: UUID, id_spot: UUID) -> bool:
        self._check_if_allowed(id_user=id_user, id_spot=id_spot)

        return super().delete(id_spot=id_spot)

    def _check_if_allowed(self, id_user: UUID, id_spot: UUID):
        spot = self.get_by_id(id_spot=id_spot)

        if spot.owner.id_user != id_user:
            raise AuthExceptionHTTPException(detail="User not allowed")

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

    def save_multiple_files(
        self, id_spot: UUID, id_user: UUID, uploaded_files: List[UploadFile]
    ) -> List[str]:
        self._check_if_allowed(id_user=id_user, id_spot=id_spot)

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
