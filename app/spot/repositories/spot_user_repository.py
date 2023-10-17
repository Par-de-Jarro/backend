from sqlalchemy.orm import Session

from app.common.repositories.base import BaseRepository
from app.spot.models.spot_user import SpotUser


class SpotUserRepository(BaseRepository):
    def __init__(self, db: Session):
        super(SpotUserRepository, self).__init__(SpotUser.id_spot_user, model_class=SpotUser, db=db)
