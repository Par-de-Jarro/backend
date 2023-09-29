import requests

from app.core.settings import GOOGLE_API_ADDRESS_KEY


class GoogleAutoCompletesApi:
    def __init__(self):
        self.base_url = "https://maps.googleapis.com/maps/api/place/autocomplete/json"
        self.auth = GOOGLE_API_ADDRESS_KEY

    def get_autocomplete_from_location(self, location: str):
        response = requests.get(self.base_url, params={"key": self.auth, "input": location}).json()[
            "predictions"
        ]

        return response
