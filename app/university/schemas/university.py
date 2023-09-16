from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class University(BaseModel):
    name: str
    slug: str
    lat: Decimal
    long: Decimal


class UniversityView(University):
    id_university: UUID

    class Config:
        orm_mode = True
