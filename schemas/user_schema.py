from pydantic import BaseModel, EmailStr
from typing import Literal


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    role: Literal["umkm", "influencer"]


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    user_id: int