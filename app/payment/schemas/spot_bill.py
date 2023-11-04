from datetime import date
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from app.common.schemas import omit
from app.spot.schemas.spot import SpotView


class SpotBill(BaseModel):
    id_spot_bill: UUID
    id_spot: UUID
    value: Decimal
    reference_date: date
    images: List[str]
    name: str
    description: Optional[str]


@omit("id_spot_bill", "images")
class SpotBillCreate(SpotBill):
    ...


class SpotBillUpdate(SpotBill):
    name: Optional[str]
    description: Optional[str]


@omit("users", "occupied_quota", "owner")
class SimplifiedSpotView(SpotView):
    ...


class SpotBillView(SpotBill):
    spot: SimplifiedSpotView
