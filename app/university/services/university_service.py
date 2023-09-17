from sqlalchemy.orm import Session

from app.common.repositories.google_address_api import GoogleAddressApi
from app.common.services.base import BaseService
from app.university.repositories.university_repository import UniversityRepository
from app.university.schemas.university import UniversityCreate, UniversityUpdate, UniversityView


class UniversityService(BaseService[UniversityCreate, UniversityUpdate, UniversityView]):
    repository: UniversityRepository
    db: Session
    google_address_api: GoogleAddressApi

    def __init__(self, db: Session):
        super().__init__(repository=UniversityRepository, db=db)
        self.google_address_api = GoogleAddressApi()
        self.db = db

    def create(self, create: UniversityCreate) -> UniversityView:
        if create.lat and create.long:
            return super().create(create)
        else:
            lat, long = self.google_address_api.get_location_coordinates(
                location=f"{create.name} - {create.slug}"
            )

            university_create = UniversityCreate(
                **create.dict(exclude={"lat", "long"}), lat=lat, long=long
            )
            return super().create(university_create)
