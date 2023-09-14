from sqlalchemy.orm import Session

from app.common.services.base import BaseService
from app.spot.repositories.spot_repository import SpotRepository
from app.spot.schemas.spot import SpotCreate, SpotUpdate, SpotView


class SpotService(BaseService[SpotCreate, SpotUpdate, SpotView]):
    repository: SpotRepository

    def __init__(self, db: Session):
        super().__init__(repository=SpotRepository, db=db)
