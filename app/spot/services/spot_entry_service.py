from uuid import UUID
from sqlalchemy.orm import Session
from app.common.exceptions import AuthExceptionHTTPException, NotAvailableSpotVacanciesException
from app.common.repositories.aws_repository import AWSRepository
from app.common.repositories.google_address_api import GoogleAddressApi
from app.common.services.base import BaseService
from app.spot.repositories.spot_entry_repository import SpotEntryRequestRepository
from app.spot.schemas.spot_entry_request import SpotEntryRequest, SpotEntryRequestCreate, UpdateStatus


class SpotEntryService(BaseService[SpotEntryRequestCreate, SpotEntryRequest, UpdateStatus]):
    repository: SpotEntryRequestRepository
    db: Session
    google_adress_api: GoogleAddressApi

    def __int__(self, db: Session):
        super().__init__(repository=SpotEntryRequestRepository, db=db)
        self.aws_repository = AWSRepository(base_path="spot")
        self.google_address_api = GoogleAddressApi()
        self.db = db

    def create(self, create: SpotEntryRequestCreate) -> None:
        return super.create(create)

    def _check_if_allowed(self, id_user: UUID, id_spot: UUID):
        spot = self.get_by_id(id_spot=id_spot)

        if spot.owner.id_user != id_user:
            raise AuthExceptionHTTPException(detail="User not allowed")

    def request_entry(self, id_user: UUID, id_spot: UUID):
        if self.repository.check_spot_availability(id_spot):
            entry = SpotEntryRequestCreate
            create_entry = SpotEntryRequestCreate(**entry.dict(id_user=id_user, id_spot=id_spot))
            return self.create(create_entry)
        else:
            raise NotAvailableSpotVacanciesException

    def accept_entry(self, id_user: UUID, id_spot: UUID, id_spot_entry_request: UUID):
        self._check_if_allowed(id_user, id_spot)

        return self.repository.accept_entry_request(id_spot_entry_request)

    def reject_entry(self, id_user: UUID, id_spot: UUID, id_spot_entry_request: UUID):
        self._check_if_allowed(id_user, id_spot)

        return self.repository.reject_entry_request(id_spot_entry_request)
