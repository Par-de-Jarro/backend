import requests

from app.core.settings import GOOGLE_API_ADDRESS_KEY


class GoogleAddressApi:
    def __init__(self):
        self.base_url = "https://maps.googleapis.com/maps/api/geocode/json"
        self.auth = GOOGLE_API_ADDRESS_KEY

    def get_location_coordinates(self, street: str, city: str, zip_code: str):
        response = requests.get(
            self.base_url, params={"key": self.auth, "address": f"{street} {city} {zip_code}"}
        ).json()["results"]

        address = response[0]
        location = address["geometry"]["location"]

        lat = location["lat"]
        lng = location["lng"]

        return (lat, lng)
