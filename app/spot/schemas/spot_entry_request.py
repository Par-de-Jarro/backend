from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class EntryRequestStatus(Enum):
    ACCEPTED = "ACCEPTED"
    NOT_ACCEPTED = "NOT_ACCEPTED"
    REQUEST = "REQUEST"


class SpotEntryRequest(BaseModel):
    status: EntryRequestStatus


class SpotEntryRequestCreate(SpotEntryRequest):
    id_user: Optional[UUID]
    id_spot: Optional[UUID]


class UpdateStatus(BaseModel):
    status: Optional[EntryRequestStatus]
