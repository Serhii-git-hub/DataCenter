from typing import Literal

from pydantic import BaseModel, Field, ConfigDict

class UserCreate(BaseModel):
    full_name: str = Field(max_length=128, min_length=3)
    login: str = Field(max_length=100, min_length=3)
    password: str = Field(min_length= 6, max_length=64)
    role: Literal["admin", "master" , "storekeeper"]

class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    full_name: str
    login: str
    role: str

class UserUpdate(BaseModel):
    password: str | None = Field(default=None, min_length=6, max_length=64)
    full_name: str | None = Field(default=None ,max_length=128, min_length=3)
    login: str | None = Field(default=None ,max_length=100, min_length=3)
    role: Literal["admin", "master", "storekeeper"] | None = None


class LoginCheck(BaseModel):
    login: str
    password: str