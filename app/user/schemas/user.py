from typing import Optional

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
    name: Optional[str]
    email: Optional[EmailStr]
    cellphone: Optional[str]
    document_id: Optional[str]
    profile_img: Optional[str]
    password: Optional[str]


class UserUpdateHashPassword(UserUpdate):
    password_hash: str


class UserCreateHashPassword(UserCreate):
    password_hash: str


class UserView(UserBase):
    class Config:
        orm_mode = True
