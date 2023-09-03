from uuid import UUID

from sqlalchemy.orm import Session

import app.common.models as models
from app.common.exceptions import RecordNotFoundException
from app.common.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db)

    def get_by_id(self, id: UUID) -> models.User:
        user = self.db.query(models.User).filter(models.User.id == id).first()
        if user is None:
            raise RecordNotFoundException(id, models.User)
        return user

    def get_by_email(self, email: str) -> models.User:
        user = self.db.query(models.User).filter(models.User.email == email).first()
        if user is None:
            raise RecordNotFoundException(email, models.User)
        return user

    def get_by_document_id(self, document_id: str) -> models.User:
        user = self.db.query(models.User).filter(models.User.document_id == document_id).first()
        if user is None:
            raise RecordNotFoundException(document_id, models.User)
        return user

    def get_by_cellphone(self, cellphone: str) -> models.User:
        user = self.db.query(models.User).filter(models.User.cellphone == cellphone).first()
        if user is None:
            raise RecordNotFoundException(cellphone, models.User)
        return user
