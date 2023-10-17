from uuid import UUID

from pydantic import BaseModel


class SpotUser(BaseModel):
    id_user: UUID
    id_spot: UUID


class SpotUserCreate(SpotUser):
    ...


class SpotUserUpdae(BaseModel):
    ...


class SpotUserView(SpotUser):
    class Config:
        orm_mode = True
