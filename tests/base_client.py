from uuid import UUID

from requests import Session


class BaseClient:
    def __init__(self, client, endpoint_path):
        self.path: str = endpoint_path
        self.client: Session = client
        self.headers = {
            **client.headers,
            "Content-type": "application/json",
        }

    def get_by_id(self, id: UUID):
        return self.client.get(f"/{self.path}/{str(id)}", headers=self.headers)

    def get_all(self):
        return self.client.get(f"/{self.path}/", headers=self.headers)

    def create(self, create):
        return self.client.post(f"/{self.path}/", data=create, headers=self.headers)

    def update(self, update, id: UUID):
        return self.client.put(f"/{self.path}/{str(id)}", data=update, headers=self.headers)

    def delete(self, id: UUID):
        return self.client.delete(f"/{self.path}/{str(id)}", headers=self.headers)
