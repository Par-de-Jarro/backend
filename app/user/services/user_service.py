from uuid import UUID

from sqlalchemy.orm import Session

from app.common.services.base import BaseService
from app.common.utils import password as password_utils
from app.user.repositories.user_repository import UserRepository
from app.user.schemas.user import UserCreate, UserCreateHashPassword, UserUpdate, UserView


class UserService(BaseService[UserCreate, UserUpdate, UserView]):
    def __init__(self, db: Session):
        super().__init__(repository=UserRepository, db=db)

    def create(self, create: UserCreate) -> UserView:
        user_create = UserCreateHashPassword(
            **create.dict(), password_hash=password_utils.create_hash(create.password)
        )

        return self.repository.add(user_create)

    def get_user_by_email(self, email: str) -> UserView:
        return self.repository.get_by_email(email)

    def get_user_by_document_id(self, document_id: str) -> UserView:
        return self.repository.get_by_document_id(document_id)

    def get_user_by_cellphone(self, cellphone: str) -> UserView:
        return self.repository.get_by_cellphone(cellphone)

    def update(self, id: UUID, update: UserUpdate) -> UserView:
        return self.repository.update(id, update)

    def update_password(self, id: UUID, update: UserUpdate) -> UserView:
        return self.repository.update_password(id, update)

    def delete(self, id: UUID) -> None:
        return self.repository.delete(id)
