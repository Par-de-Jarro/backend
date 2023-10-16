from uuid import UUID

from sqlalchemy.orm import Session

from app.common.exceptions import AuthExceptionHTTPException, NotAvailableSpotVacanciesException
from app.common.services.base import BaseService
from app.spot.repositories.spot_entry_repository import SpotEntryRequestRepository
from app.spot.schemas.spot_entry_request import (
    EntryRequestStatus,
    SpotEntryRequestCreate,
    SpotEntryRequestUpdate,
    SpotEntryView,
)
from app.spot.services.spot_service import SpotService


class SpotEntryService(BaseService[SpotEntryRequestCreate, SpotEntryRequestUpdate, SpotEntryView]):
    repository: SpotEntryRequestRepository
    spot_service: SpotService

    def __init__(self, db: Session):
        super().__init__(repository=SpotEntryRequestRepository, db=db)
        self.db = db

    def _check_if_allowed(self, id_user: UUID, id_spot: UUID):
        spot = self.spot_service.get_by_id(id_spot=id_spot)
        if spot.owner.id_user != id_user:
            raise AuthExceptionHTTPException(detail="User not allowed")

    def request_entry(self, id_user: UUID, id_spot: UUID):
        if self.repository.check_spot_availability(id_spot):  # TODO
            return self.create(
                create=SpotEntryRequestCreate(
                    id_user=id_user, id_spot=id_spot, status=EntryRequestStatus.REQUEST
                )
            )
        else:
            raise NotAvailableSpotVacanciesException

    def accept_entry(self, id_user: UUID, id_spot: UUID, id_spot_entry_request: UUID):
        self._check_if_allowed(id_user, id_spot)

        if self.repository.check_spot_availability(id_spot):  # TODO
            request = self.update(
                id_spot_entry_request=id_spot_entry_request,
                update=SpotEntryRequestUpdate(status=EntryRequestStatus.ACCEPTED),
            )
            # self.repository.user_spot_association(id_user, id_spot)  # TODO
            return request
        else:
            raise NotAvailableSpotVacanciesException

    def reject_entry(self, id_user: UUID, id_spot: UUID, id_spot_entry_request: UUID):
        self._check_if_allowed(id_user, id_spot)
        return self.update(
            id_spot_entry_request=id_spot_entry_request,
            update=SpotEntryRequestUpdate(status=EntryRequestStatus.NOT_ACCEPTED),
        )
