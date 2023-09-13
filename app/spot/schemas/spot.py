from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel


class Images(BaseModel):
    image_url: str
    image_order: int


class SpotKey(BaseModel):
    convenience: ...
    # quantos quartos,
    # quantos banheiros,


class Spot(BaseModel):
    name: str
    description: str
    personal_quota: int
    images: Optional[List[Images]]
    value: Decimal
    lat: Decimal
    long: Decimal
    street: str
    number: str
    complement: str
    city: str
    state: str
    observations: str
    key = ...


# se é apartamento ou casa,
# se for apartamento: se tem elevador e em qual andar fica
# se permite fumantes
# se permite pets
# se permite pets
