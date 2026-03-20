from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: datetime


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    appointment_date: datetime | None = None
    status: str | None = Field(default=None, min_length=3, max_length=20)


class AppointmentOut(AppointmentBase):
    id: int
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
