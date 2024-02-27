from enum import Enum
from typing import Optional
from uuid import UUID

from fastapi_qp import QueryParam
from pydantic import BaseModel

from app.spot.schemas.spot import SpotView
from app.user.schemas.user import UserView


class EntryRequestStatus(Enum):
    ACCEPTED = "ACCEPTED"
    NOT_ACCEPTED = "NOT_ACCEPTED"
    REQUEST = "REQUEST"
    CANCELLED = "CANCELLED"


class SpotEntryRequest(BaseModel):
    id_user: UUID
    id_spot: UUID
    status: EntryRequestStatus


class SpotEntryRequestCreate(SpotEntryRequest):
    ...


class SpotEntryView(SpotEntryRequest):
    id_spot_entry_request: UUID
    user: UserView
    spot: SpotView

    class Config:
        orm_mode = True


class SpotEntryRequestUpdate(BaseModel):
    status: Optional[EntryRequestStatus]


class SpotEntryRequestGetParams(BaseModel, QueryParam):
    id_user: Optional[UUID]
    id_owner: Optional[UUID]
    id_spot: Optional[UUID]
    status: Optional[EntryRequestStatus]
