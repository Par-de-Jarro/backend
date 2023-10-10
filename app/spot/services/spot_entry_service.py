from uuid import UUID
from sqlalchemy.orm import Session
from app.common.exceptions import AuthExceptionHTTPException, NotAvailableSpotVacanciesException
from app.common.services.base import BaseService
from app.spot.repositories.spot_entry_repository import SpotEntryRequestRepository
from app.spot.schemas.spot_entry_request import SpotEntryRequest, SpotEntryRequestCreate, UpdateStatus, \
    EntryRequestStatus
from app.spot.services.spot_service import SpotService


class SpotEntryService(BaseService[SpotEntryRequestCreate, SpotEntryRequest, UpdateStatus]):
    repository: SpotEntryRequestRepository
    db: Session
    spot_service: SpotService

    def __init__(self, db: Session):
        super().__init__(repository=SpotEntryRequestRepository, db=db)
        self.db = db

    def create(self, create: SpotEntryRequestCreate) -> None:
        return super.create(create)

    def _check_if_allowed(self, id_user: UUID, id_spot: UUID):
        spot = self.spot_service.get_by_id(id_spot=id_spot)

        if spot.owner.id_user != id_user:
            raise AuthExceptionHTTPException(detail="User not allowed")

    def update(self, id_user: UUID, id_spot: UUID, id_spot_entry_request: UUID, update: UpdateStatus):
        self._check_if_allowed(id_user, id_spot)

        return super().update(update=update, id_spot_entry_request=id_spot_entry_request)

    def request_entry(self, id_user: UUID, id_spot: UUID):
        if self.repository.check_spot_availability(id_spot):
            entry = SpotEntryRequestCreate
            create_entry = SpotEntryRequestCreate(**entry.dict(id_user=id_user, id_spot=id_spot))
            return self.create(create_entry)
        else:
            raise NotAvailableSpotVacanciesException

    def accept_entry(self, id_user: UUID, id_spot: UUID, id_spot_entry_request: UUID):
        self._check_if_allowed(id_user, id_spot)
        status = EntryRequestStatus.ACCEPTED
        update = UpdateStatus(status=status)
        self.update(id_user, id_spot, id_spot_entry_request, update)

        return self.repository.user_spot_association(id_user, id_spot)

    def reject_entry(self, id_user: UUID, id_spot: UUID, id_spot_entry_request: UUID):
        self._check_if_allowed(id_user, id_spot)
        status = EntryRequestStatus.NOT_ACCEPTED
        update = UpdateStatus(status=status)
        return self.update(id_user, id_spot, id_spot_entry_request, update)
