from typing import Optional

from sqlalchemy.orm import Session

import app.common.models as models
from app.common.repositories.base import BaseFinder, BaseRepository
from app.user.models.user import User


class UserFinder(BaseFinder[User]):
    @classmethod
    def get_instance(cls, db: Session):
        return cls((db.query(UserFinder).filter(User.deleted_at.is_(None))))

    def filter_by_email(self, email: Optional[str]):
        if email:
            return UserFinder(self.base_query.filter(User.email == email))
        return self

    def filter_by_document_id(self, document_id: Optional[str]):
        if document_id:
            return UserFinder(self.base_query.filter(User.document_id == document_id))
        return self

    def filter_by_cellphone(self, cellphone: Optional[str]):
        if cellphone:
            return UserFinder(self.base_query.filter(User.cellphone == cellphone))
        return self


class UserRepository(BaseRepository):
    finder: UserFinder

    def __init__(self, db: Session):
        super(UserRepository, self).__init__(
            models.User.id_user,
            model_class=models.User,
            finder=UserFinder,
            db=db,
        )
