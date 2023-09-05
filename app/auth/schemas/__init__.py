from datetime import datetime

from pydantic import BaseModel, Field

from app.user.schemas.user import UserView

email_field = Field(
    regex="([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+([A-Z|a-z]{2,})+"
)  # noqa: W605


class SessionCreate(BaseModel):
    email: str = email_field
    password: str


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: UserView


class TokenPayload(BaseModel):
    exp: datetime
    sub: str
    email: str = email_field
    id_user: str
    name: str
