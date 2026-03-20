from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class MedicalRecordBase(BaseModel):
    patient_id: int
    diagnosis: str = Field(..., min_length=2, max_length=255)
    treatment: str = Field(..., min_length=2)
    date: datetime | None = None


class MedicalRecordCreate(MedicalRecordBase):
    pass


class MedicalRecordUpdate(BaseModel):
    diagnosis: str | None = Field(default=None, min_length=2, max_length=255)
    treatment: str | None = Field(default=None, min_length=2)
    date: datetime | None = None


class MedicalRecordOut(MedicalRecordBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
