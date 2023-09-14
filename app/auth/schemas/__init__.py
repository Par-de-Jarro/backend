from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.user.schemas.user import UserView


class SessionCreate(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: UserView


class TokenPayload(BaseModel):
    exp: datetime
    sub: str
    email: EmailStr
    id_user: str
    name: str
