from datetime import date
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from fastapi_qp import QueryParam
from pydantic import BaseModel

from app.common.schemas import omit
from app.spot.schemas.spot import SpotView


class SpotBill(BaseModel):
    id_spot_bill: UUID
    id_spot: UUID
    value: Decimal
    reference_date: date
    images: Optional[List[str]] = []
    name: str
    description: Optional[str]


@omit("id_spot_bill", "images")
class SpotBillCreate(SpotBill):
    ...


class SpotBillUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    images: List[str]


@omit("users", "occupied_quota", "owner", "is_available")
class SimplifiedSpotView(SpotView):
    ...


class SpotBillView(SpotBill):
    spot: SimplifiedSpotView

    class Config:
        orm_mode = True


class SpotBillGetParams(BaseModel, QueryParam):
    id_owner: Optional[UUID]
    id_spot: Optional[UUID]
    reference_date_start: Optional[date]
    reference_date_end: Optional[date]
