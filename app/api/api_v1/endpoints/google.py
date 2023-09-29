from typing import List

from fastapi import APIRouter, Depends, Security

import app.api.deps as deps
from app.google.schemas.google import AutoCompletePayload, GeoCode
from app.google.services.google import GoogleService

router = APIRouter()
validate_token = deps.token_auth()


@router.get(
    "/autocomplete",
    dependencies=[Security(validate_token)],
    response_model=List[AutoCompletePayload],
)
def auto_complete(location: str, service: GoogleService = Depends(deps.get_google_service)):
    return service.get_autocomplete_from_location(location)


@router.get(
    "/geocode",
    dependencies=[Security(validate_token)],
    response_model=GeoCode,
)
def geocode(location: str, service: GoogleService = Depends(deps.get_google_service)):
    return service.get_geo_code(location)
