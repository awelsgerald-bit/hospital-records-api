from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

UserRole = Literal["admin", "doctor", "receptionist"]


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    full_name: str | None = Field(default=None, max_length=150)
    password: str = Field(..., min_length=6, max_length=100)
    role: UserRole = "receptionist"


class UserOut(BaseModel):
    id: int
    username: str
    full_name: str | None
    role: UserRole
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class UserCreateByAdmin(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    full_name: str | None = Field(default=None, max_length=150)
    password: str = Field(..., min_length=6, max_length=100)
    role: UserRole
