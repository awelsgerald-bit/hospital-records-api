from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db, require_roles
from app.models.medical_record import MedicalRecord
from app.models.patient import Patient
from app.models.user import User
from app.schemas.medical_record import (
    MedicalRecordCreate,
    MedicalRecordOut,
    MedicalRecordUpdate,
)

router = APIRouter(prefix="/medical-records", tags=["Medical Records"])


@router.post("/", response_model=MedicalRecordOut, status_code=status.HTTP_201_CREATED)
def add_medical_record(
    payload: MedicalRecordCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("admin", "doctor")),
):
    patient = db.query(Patient).filter(Patient.id == payload.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    data = payload.model_dump()
    if data["date"] is None:
        data["date"] = datetime.utcnow()

    record = MedicalRecord(**data)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/", response_model=list[MedicalRecordOut])
def get_all_medical_records(
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("admin", "doctor")),
):
    return db.query(MedicalRecord).order_by(MedicalRecord.id.desc()).all()


@router.get("/patient/{patient_id}", response_model=list[MedicalRecordOut])
def get_patient_medical_history(
    patient_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("admin", "doctor")),
):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    return (
        db.query(MedicalRecord)
        .filter(MedicalRecord.patient_id == patient_id)
        .order_by(MedicalRecord.date.desc())
        .all()
    )


@router.get("/{record_id}", response_model=MedicalRecordOut)
def get_medical_record(
    record_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("admin", "doctor")),
):
    record = db.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Medical record not found")
    return record


@router.put("/{record_id}", response_model=MedicalRecordOut)
def update_medical_record(
    record_id: int,
    payload: MedicalRecordUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("admin", "doctor")),
):
    record = db.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Medical record not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(record, key, value)

    db.commit()
    db.refresh(record)
    return record


@router.delete("/{record_id}")
def delete_medical_record(
    record_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("admin")),
):
    record = db.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Medical record not found")

    db.delete(record)
    db.commit()
    return {"message": "Medical record deleted successfully"}
