from sqlalchemy.orm import Session

from app.common.services.base import BaseService
from app.spot.repositories.spot_user_repository import SpotUserRepository
from app.spot.schemas.spot_user import SpotUserCreate, SpotUserUpdae, SpotUserView


class SpotUserService(BaseService[SpotUserCreate, SpotUserUpdae, SpotUserView]):
    repository: SpotUserRepository
    db: Session

    def __init__(self, db: Session):
        super().__init__(repository=SpotUserRepository, db=db)
