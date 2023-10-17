from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class EntryRequestStatus(Enum):
    ACCEPTED = "ACCEPTED"
    NOT_ACCEPTED = "NOT_ACCEPTED"
    REQUEST = "REQUEST"


class SpotEntryRequest(BaseModel):
    id_user: UUID
    id_spot: UUID
    status: EntryRequestStatus


class SpotEntryRequestCreate(SpotEntryRequest):
    ...


class SpotEntryView(SpotEntryRequest):
    id_spot_entry_request: UUID

    class Config:
        orm_mode = True


class SpotEntryRequestUpdate(BaseModel):
    status: Optional[EntryRequestStatus]
