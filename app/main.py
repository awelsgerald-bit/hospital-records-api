from fastapi import FastAPI
from fastapi.responses import FileResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.database.db import Base, SessionLocal, engine
from app.models import appointment, doctor, doctor_patient_assignment, medical_record, patient, user
from app.models.user import User
from app.routes.appointments import router as appointments_router
from app.routes.auth import router as auth_router
from app.routes.doctors import router as doctors_router
from app.routes.medical_records import router as medical_records_router
from app.routes.patients import router as patients_router

# Ensure all model metadata is imported before creating tables.
_ = (appointment, doctor, doctor_patient_assignment, medical_record, patient, user)

app = FastAPI(
    title="Hospital Records Management API",
    description="Beginner-friendly but production-structured REST API for hospital records.",
    version="1.0.0",
)


def seed_default_admin(db: Session) -> None:
    """Create a default admin account for quick local testing."""
    admin = db.query(User).filter(User.username == "admin").first()
    if admin:
        if admin.role != "admin":
            admin.role = "admin"
            db.commit()
        return

    db.add(
        User(
            username="admin",
            full_name="System Admin",
            hashed_password=get_password_hash("admin123"),
            role="admin",
        )
    )
    db.commit()


def ensure_user_role_column() -> None:
    """
    Lightweight startup migration for existing SQLite databases created
    before role-based access control was introduced.
    """
    with engine.begin() as conn:
        rows = conn.execute(text("PRAGMA table_info(users)")).mappings().all()
        columns = {row["name"] for row in rows}
        if "role" not in columns:
            conn.execute(
                text(
                    "ALTER TABLE users ADD COLUMN role VARCHAR(30) NOT NULL DEFAULT 'receptionist'"
                )
            )


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    ensure_user_role_column()
    db = SessionLocal()
    try:
        seed_default_admin(db)
    finally:
        db.close()


@app.get("/")
def dashboard():
    return FileResponse("app/static/index.html")


@app.get("/health")
def health_check():
    return {"message": "Hospital Records Management API is running"}


app.include_router(auth_router)
app.include_router(patients_router)
app.include_router(doctors_router)
app.include_router(appointments_router)
app.include_router(medical_records_router)
