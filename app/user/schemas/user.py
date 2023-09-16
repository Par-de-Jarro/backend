from datetime import date
from typing import Optional
from uuid import UUID

from fastapi_qp import QueryParam
from pydantic import BaseModel, EmailStr, Field

from app.common.schemas import omit
from app.university.schemas.university import UniversityView

cellphone_field = Field(min_length=11, max_length=11)
document_id_field = Field(min_length=11, max_length=11)


class UserBase(BaseModel):
    name: str
    email: EmailStr
    cellphone: str = cellphone_field
    document_id: str = document_id_field
    profile_img: Optional[str]
    birthdate: date
    course: str
    bio: str


@omit("profile_img")
class UserCreate(UserBase):
    password: str
    id_university: UUID


class UserUpdate(UserBase):
    name: Optional[str]
    email: Optional[EmailStr]
    cellphone: Optional[str]
    document_id: Optional[str]
    profile_img: Optional[str]
    password: Optional[str]
    birthdate: Optional[date]
    course: Optional[str]
    bio: Optional[str]
    id_university: Optional[UUID]


@omit("password")
class UserUpdateHashPassword(UserUpdate):
    password_hash: str


@omit("password")
class UserCreateHashPassword(UserCreate):
    password_hash: str


class UserView(UserBase):
    id_user: UUID
    university: UniversityView

    class Config:
        orm_mode = True


class UserSearchParams(BaseModel, QueryParam):
    email: Optional[EmailStr]
    cellphone: Optional[str] = cellphone_field
    document_id: Optional[str] = document_id_field
