from decimal import Decimal
from enum import Enum
from typing import List, Optional
from uuid import UUID

from fastapi_qp import QueryParam
from pydantic import BaseModel, Field

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
    description: Optional[str]
    personal_quota: int
    images: Optional[List[Images]]
    type: SpotType
    value: Decimal
    lat: Decimal
    long: Decimal
    street: str
    zip_code: str
    number: str
    complement: Optional[str]
    city: str
    state: str
    key: SpotKey


class SpotView(Spot):
    id_spot: UUID
    owner: Optional[UserView]
    users: Optional[List[UserView]]
    is_available: Optional[bool]
    occupied_quota: Optional[int]

    class Config:
        orm_mode = True


@omit("users", "occupied_quota", "owner", "is_available")
class SimplifiedSpotView(SpotView):
    ...


class SpotSearchView(BaseModel):
    Spot: SimplifiedSpotView
    distance: Optional[Decimal]


@omit("images")
class SpotCreate(Spot):
    id_user: Optional[UUID]
    lat: Optional[Decimal]
    long: Optional[Decimal]


class SpotUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    personal_quota: Optional[int]
    type: Optional[SpotType]
    value: Optional[Decimal]
    key: Optional[SpotKey]
    images: Optional[List[Images]]


class SpotSearchParams(BaseModel, QueryParam):
    lat: Optional[Decimal]
    long: Optional[Decimal]
    type: Optional[SpotType]
    allow_pet: Optional[bool]
    allow_smoker: Optional[bool]
    rooms_quantity: Optional[int]
    bathrooms_quantity: Optional[int]
    has_elevator: Optional[bool]
    value_max: Optional[Decimal]
    value_min: Optional[Decimal]
    distance_range: Optional[Decimal] = Field(default=10)


class SpotGetParams(BaseModel, QueryParam):
    id_user: Optional[UUID]
