from sqlalchemy.orm import Session

import app.common.models as models
from app.common.repositories.base import BaseRepository


class SpotRepository(BaseRepository):
    def __init__(self, db: Session):
        super(SpotRepository, self).__init__(
            models.Spot.id_spot,
            model_class=models.Spot,
            db=db,
        )
