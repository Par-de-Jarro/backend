from sqlalchemy.orm import Session

from app.common.repositories.base import BaseRepository
from app.university.models.university import University


class UniversityRepository(BaseRepository):
    def __init__(self, db: Session):
        super(UniversityRepository, self).__init__(
            University.id_university,
            model_class=University,
            db=db,
        )
