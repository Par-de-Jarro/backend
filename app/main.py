from datetime import date, datetime
from decimal import Decimal
from json import JSONEncoder
from uuid import UUID

from fastapi import FastAPI

from .api.api_v1.api import api_router as v1_api_router

default_json_encoder = JSONEncoder.default


def custom_json_encoder(self, obj):
    if isinstance(obj, UUID) or isinstance(obj, Decimal):
        return str(obj)
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    return default_json_encoder(self, obj)


JSONEncoder.default = custom_json_encoder

app = FastAPI(
    title="Todo List API",
)

app.include_router(v1_api_router)
