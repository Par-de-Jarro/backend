from sqlalchemy.orm import Session

from app.common.repositories.base import BaseFinder, BaseRepository
from app.spot.models.spot import Spot


class SpotFinder(BaseFinder[Spot]):
    ...


class SpotRepository(BaseRepository):
    finder: SpotFinder

    def __init__(self, db: Session):
        super(SpotRepository, self).__init__(
            Spot.id_spot, model_class=Spot, db=db, finder=SpotFinder
        )
