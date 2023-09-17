from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class University(BaseModel):
    name: str
    slug: str
    lat: Decimal
    long: Decimal


class UniversityCreate(University):
    lat: Optional[Decimal]
    long: Optional[Decimal]


class UniversityUpdate(BaseModel):
    name: Optional[str]
    slug: Optional[str]
    lat: Optional[Decimal]
    long: Optional[Decimal]


class UniversityView(University):
    id_university: UUID

    class Config:
        orm_mode = True
