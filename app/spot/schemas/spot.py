from decimal import Decimal
from enum import Enum
from typing import List, Optional
from uuid import UUID

from fastapi_qp import QueryParam
from pydantic import BaseModel

from app.common.schemas import omit
from app.user.schemas.user import UserView


class Images(BaseModel):
    image_url: str
    image_order: int


class SpotConvenience(BaseModel):
    rooms_quantity: Optional[int]
    bathrooms_quantity: Optional[int]
    has_elevator: Optional[bool]


class SpotAllowance(BaseModel):
    allow_pet: Optional[bool]
    allow_smoker: Optional[bool]


class SpotKey(BaseModel):
    convenience: SpotConvenience
    allowance: SpotAllowance


class SpotType(Enum):
    HOUSE = "house"
    APARTMENT = "apartment"


class Spot(BaseModel):
    name: str
    description: str
    personal_quota: int
    images: Optional[List[Images]]
    type: SpotType
    value: Decimal
    lat: Decimal
    long: Decimal
    street: str
    zip_code: str
    number: str
    complement: str
    city: str
    state: str
    observations: str
    key: SpotKey


class SpotView(Spot):
    id_spot: UUID
    owner: UserView
    distance: Optional[Decimal]

    class Config:
        orm_mode = True


@omit("images")
class SpotCreate(Spot):
    id_user: UUID


class SpotUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    personal_quota: Optional[int]
    type: Optional[SpotType]
    value: Optional[Decimal]
    observations: Optional[str]
    key: Optional[SpotKey]
    images: Optional[List[Images]]


class SpotSearchParams(BaseModel, QueryParam):
    lat: Optional[Decimal]
    long: Optional[Decimal]
    type: Optional[SpotType]
    allow_pet: Optional[bool]
    allow_smoker: Optional[bool]
    rooms_quantity_max: Optional[int]
    rooms_quantity_min: Optional[int]
    bathrooms_quantity_max: Optional[int]
    bathrooms_quantity_min: Optional[int]
    has_elevator: Optional[bool]
    value_max: Optional[Decimal]
    value_min: Optional[Decimal]
    distance_range: Optional[Decimal]
