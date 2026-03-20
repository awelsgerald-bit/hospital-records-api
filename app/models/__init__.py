from app.models.appointment import Appointment
from app.models.doctor import Doctor
from app.models.doctor_patient_assignment import DoctorPatientAssignment
from app.models.medical_record import MedicalRecord
from app.models.patient import Patient
from app.models.user import User

__all__ = [
    "Appointment",
    "Doctor",
    "DoctorPatientAssignment",
    "MedicalRecord",
    "Patient",
    "User",
]
