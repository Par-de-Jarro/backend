from typing import Generic, List, TypeVar

from sqlalchemy.orm import Session

from app.common.repositories.base import BaseRepository

T = TypeVar("T")
ID = TypeVar("ID")

CREATE = TypeVar("CREATE")
UPDATE = TypeVar("UPDATE")
RETURN = TypeVar("RETURN")


def make_repository(repository, db: Session):
    return repository(db)


class BaseService(Generic[CREATE, UPDATE, RETURN]):
    def __init__(self, repository: BaseRepository, db: Session):
        self.repository = make_repository(repository=repository, db=db)

    def get_by_id(self, **kwargs) -> RETURN:
        return self.repository.get_by_id(**kwargs)

    def get_all(self) -> List[RETURN]:
        return self.repository.get_all()

    def create(self, create: CREATE) -> RETURN:
        return self.repository.add(create)

    def update(self, update: UPDATE, **kwargs) -> RETURN:
        return self.repository.update(update, **kwargs)

    def delete(self, **kwargs) -> bool:
        return self.repository.delete(**kwargs)
