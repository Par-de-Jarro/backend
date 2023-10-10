from uuid import UUID

from sqlalchemy.orm import Session

from app.common.services.base import BaseService
from app.spot.models.spot_user import SpotUser


class SpotUserService(BaseService[SpotUser]):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def associate(self, id_user: UUID, id_spot: UUID):
        spot_user = SpotUser(id_user, id_spot)
        self.db_session.add(spot_user)
        self.db_session.commit()
        return spot_user

    def count_users_in_spot(self, id_spot: UUID):
        count = self.db_session.query(SpotUser).filter_by(id_spot=id_spot).count()
        return count
