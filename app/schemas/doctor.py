from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DoctorBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    specialization: str = Field(..., min_length=2, max_length=120)
    contact: str = Field(..., min_length=5, max_length=50)


class DoctorCreate(DoctorBase):
    pass


class DoctorUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    specialization: str | None = Field(default=None, min_length=2, max_length=120)
    contact: str | None = Field(default=None, min_length=5, max_length=50)


class DoctorOut(DoctorBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DoctorPatientAssign(BaseModel):
    doctor_id: int
    patient_id: int


class DoctorPatientAssignOut(BaseModel):
    id: int
    doctor_id: int
    patient_id: int
    assigned_at: datetime

    model_config = ConfigDict(from_attributes=True)
