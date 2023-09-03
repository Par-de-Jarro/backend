from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

cellphone_field = Field(min_length=13, max_length=13)
document_id_field = Field(min_length=11, max_length=11)


class UserBase(BaseModel):
    name: str
    email: EmailStr
    cellphone: str = cellphone_field
    document_id: str = document_id_field
    profile_img: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    name: str
    email: EmailStr
    cellphone: str
    document_id: str
    profile_img: str


class UserUpdatePassWord(UserBase):
    password: Optional[str]


class UserCreateHashPassword(UserBase):
    password_hash: str


class UserView(UserBase):
    name: str
    email: EmailStr
    cellphone: str
    document_id: str
    profile_img: str

    class Config:
        orm_mode = True
