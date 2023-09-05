from typing import List
from uuid import UUID

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.common.exceptions import RecordNotFoundException
from app.common.repositories.aws_repository import AWSRepository
from app.common.services.base import BaseService
from app.common.utils import password as password_utils
from app.user.repositories.user_repository import UserRepository
from app.user.schemas.user import (
    UserCreate,
    UserCreateHashPassword,
    UserSearchParams,
    UserUpdate,
    UserUpdateHashPassword,
    UserView,
)


class UserService(BaseService[UserCreate, UserUpdate, UserView]):
    repository: UserRepository

    def __init__(self, db: Session):
        super().__init__(repository=UserRepository, db=db)
        self.aws_repository = AWSRepository(base_path="user")

    def create(self, create: UserCreate) -> UserView:
        create = UserCreateHashPassword(
            **create.dict(exclude={"password"}),
            password_hash=password_utils.create_hash(create.password),
        )

        return self.repository.add(create)

    def update(self, update: UserUpdate, **kwargs) -> UserView:
        if update.password:
            update = UserUpdateHashPassword(
                **update.dict(), password_hash=password_utils.create_hash(update.password)
            )

        return super().update(update, **kwargs)

    def get_all(self, params: UserSearchParams) -> List[UserView]:
        query = self.repository.finder

        if params.cellphone:
            query = query.filter_by_cellphone(cellphone=params.cellphone)

        if params.email:
            query = query.filter_by_email(email=params.email)

        if params.document_id:
            query = query.filter_by_document_id(document_id=params.document_id)

        return query.all()

    def save_file(self, id_user: UUID, uploaded_file: UploadFile) -> UserView:
        if not (self.get_by_id(id_user=id_user)):
            print("NO")
            raise RecordNotFoundException()
        profile_image_url = self.aws_repository.save_file(
            id_obj=id_user, uploaded_file=uploaded_file
        )
        return self.update(id_user=id_user, update=UserUpdate(profile_img=profile_image_url))
