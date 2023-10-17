from uuid import UUID

from sqlalchemy.orm import Session

from app.common.exceptions import (
    AuthExceptionHTTPException,
    NotAvailableSpotVacanciesException,
    SpotEntryRequestAlreadyAccepted,
    SpotEntryRequestAlreadyDenied,
)
from app.common.services.base import BaseService
from app.spot.repositories.spot_entry_repository import SpotEntryRequestRepository
from app.spot.schemas.spot_entry_request import (
    EntryRequestStatus,
    SpotEntryRequestCreate,
    SpotEntryRequestUpdate,
    SpotEntryView,
)
from app.spot.schemas.spot_user import SpotUserCreate
from app.spot.services.spot_service import SpotService
from app.spot.services.spot_user_service import SpotUserService


class SpotEntryService(BaseService[SpotEntryRequestCreate, SpotEntryRequestUpdate, SpotEntryView]):
    repository: SpotEntryRequestRepository
    spot_service: SpotService
    spot_user_service: SpotUserService

    def __init__(self, db: Session):
        super().__init__(repository=SpotEntryRequestRepository, db=db)
        self.spot_service = SpotService(db=db)
        self.spot_user_service = SpotUserService(db=db)
        self.db = db

    def _check_if_allowed(self, id_user: UUID, id_spot: UUID):
        spot = self.spot_service.get_by_id(id_spot=id_spot)
        if spot.owner.id_user != id_user:
            raise AuthExceptionHTTPException(detail="User not allowed")

    def request_entry(self, id_user: UUID, id_spot: UUID):
        if self.spot_service.check_spot_availability(id_spot=id_spot):
            return self.create(
                create=SpotEntryRequestCreate(
                    id_user=id_user, id_spot=id_spot, status=EntryRequestStatus.REQUEST
                )
            )
        else:
            raise NotAvailableSpotVacanciesException

    def accept_entry(self, id_user: UUID, id_spot_entry_request: UUID):
        request = self.get_by_id(id_spot_entry_request=id_spot_entry_request)
        self._check_if_allowed(id_user, request.id_spot)

        if request.status == EntryRequestStatus.ACCEPTED:
            raise SpotEntryRequestAlreadyAccepted

        if request.status == EntryRequestStatus.NOT_ACCEPTED:
            raise SpotEntryRequestAlreadyDenied

        if self.spot_service.check_spot_availability(id_spot=request.id_spot):
            request = self.update(
                id_spot_entry_request=id_spot_entry_request,
                update=SpotEntryRequestUpdate(status=EntryRequestStatus.ACCEPTED),
            )
            self.spot_user_service.create(
                create=SpotUserCreate(id_spot=request.id_spot, id_user=request.id_user)
            )
            return request
        else:
            raise NotAvailableSpotVacanciesException

    def reject_entry(self, id_user: UUID, id_spot_entry_request: UUID):
        request = self.get_by_id(id_spot_entry_request=id_spot_entry_request)
        self._check_if_allowed(id_user, request.id_spot)

        if request.status == EntryRequestStatus.ACCEPTED:
            raise SpotEntryRequestAlreadyAccepted

        if request.status == EntryRequestStatus.NOT_ACCEPTED:
            raise SpotEntryRequestAlreadyDenied

        return self.update(
            id_spot_entry_request=id_spot_entry_request,
            update=SpotEntryRequestUpdate(status=EntryRequestStatus.NOT_ACCEPTED),
        )
