from typing import List

from app.common.repositories.google_address_api import GoogleAddressApi
from app.common.repositories.google_places_api import GoogleAutoCompletesApi
from app.google.schemas.google import AutoCompletePayload, GeoCode


class GoogleService:
    def __init__(self) -> None:
        self.google_auto_compleote_api = GoogleAutoCompletesApi()
        self.google_geocode_aoi = GoogleAddressApi()

    def get_autocomplete_from_location(self, location: str) -> List[AutoCompletePayload]:
        api_response = self.google_auto_compleote_api.get_autocomplete_from_location(
            location=location
        )

        return [
            AutoCompletePayload(
                description=item["description"], term=item["structured_formatting"]["main_text"]
            )
            for item in api_response
        ]

    def get_geo_code(self, location: str) -> GeoCode:
        api_response = self.google_geocode_aoi.get_location_coordinates(location=location)

        return GeoCode(location=location, lat=api_response[0], long=api_response[1])
