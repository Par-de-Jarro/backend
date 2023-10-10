
from uuid import UUID
from app.common.repositories.base import BaseRepository
from app.spot.schemas.spot_entry_request import UpdateStatus
from app.spot.services.spot_service import SpotService
from app.spot.services.spot_user_service import SpotUserService


class SpotEntryRequestRepository(BaseRepository):
    spot_user: SpotUserService
    spot: SpotService
    spot_entry_request_schema: UpdateStatus

    def check_spot_availability(self, id_spot: UUID):
        return self.spot_user.count_users_in_spot(id_spot) < self.spot.get_by_id(id_spot).personal_quota

    def user_spot_association(self, id_user: UUID, id_spot: UUID):
        return self.spot_user.associate(id_user, id_spot)
