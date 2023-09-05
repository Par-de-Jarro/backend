from sqlalchemy.orm import Session

from app.common.services.base import BaseService
from app.common.utils import password as password_utils
from app.user.repositories.user_repository import UserRepository
from app.user.schemas.user import (
    UserCreate,
    UserCreateHashPassword,
    UserUpdate,
    UserUpdateHashPassword,
    UserView,
)


class UserService(BaseService[UserCreate, UserUpdate, UserView]):
    repository: UserRepository

    def __init__(self, db: Session):
        super().__init__(repository=UserRepository, db=db)

    def create(self, create: UserCreate) -> UserView:
        create = UserCreateHashPassword(
            **create.dict(), password_hash=password_utils.create_hash(create.password)
        )

        return self.repository.add(create)

    def update(self, update: UserUpdate, **kwargs) -> UserView:
        if update.password:
            update = UserUpdateHashPassword(
                **update.dict(), password_hash=password_utils.create_hash(update.password)
            )

        return super().update(update, **kwargs)
