from decimal import Decimal

from pydantic import BaseModel


class AutoCompletePayload(BaseModel):
    description: str
    term: str


class GeoCode(BaseModel):
    location: str
    lat: Decimal
    long: Decimal
