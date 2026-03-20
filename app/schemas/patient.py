from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PatientBase(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=150)
    age: int = Field(..., ge=0, le=130)
    gender: str = Field(..., min_length=1, max_length=20)
    phone: str = Field(..., min_length=5, max_length=30)
    address: str = Field(..., min_length=3, max_length=255)


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=150)
    age: int | None = Field(default=None, ge=0, le=130)
    gender: str | None = Field(default=None, min_length=1, max_length=20)
    phone: str | None = Field(default=None, min_length=5, max_length=30)
    address: str | None = Field(default=None, min_length=3, max_length=255)


class PatientOut(PatientBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
