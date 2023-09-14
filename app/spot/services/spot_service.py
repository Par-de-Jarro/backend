from decimal import Decimal

from sqlalchemy.orm import Session

from app.common.repositories.base import haversine
from app.common.services.base import BaseService
from app.spot.models.spot import Spot
from app.spot.repositories.spot_repository import SpotFinder, SpotRepository
from app.spot.schemas.spot import SpotCreate, SpotSearchParams, SpotUpdate, SpotView
from app.user.models.user import User
from app.user.schemas.user import UserView


class SpotService(BaseService[SpotCreate, SpotUpdate, SpotView]):
    repository: SpotRepository
    db: Session

    def __init__(self, db: Session):
        super().__init__(repository=SpotRepository, db=db)
        self.db = db

    def search(self, filters: SpotSearchParams):
        finder = SpotFinder(self._get_base_query(lat=filters.lat, long=filters.long))

        return [self._parse_result(item) for item in finder.all()]

    def _parse_result(self, result) -> SpotView:
        return SpotView(**result, owner=UserView(**result["User"].__dict__))

    def _get_base_query(self, lat: Decimal, long: Decimal):
        return (
            self.db.query(
                Spot.__table__,
                haversine(Spot.lat, Spot.long, lat, long).label("distance"),
            )
            .add_entity(User)
            .filter(Spot.deleted_at.is_(None))
            .order_by("distance")
        )
