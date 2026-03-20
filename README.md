# Hospital Records Management API

Production-structured backend project for managing hospital operations: patients, doctors, appointments, and medical history.

## Live Project

- Dashboard: [https://hospital-records-api.onrender.com/](https://hospital-records-api.onrender.com/)
- API Docs (Swagger): [https://hospital-records-api.onrender.com/docs](https://hospital-records-api.onrender.com/docs)
- Health Check: [https://hospital-records-api.onrender.com/health](https://hospital-records-api.onrender.com/health)

## Project Highlights

- REST API built with **FastAPI**
- **JWT authentication** with role-based authorization
- **SQLAlchemy ORM** data layer
- Works locally with **SQLite**
- Deployment-ready with **PostgreSQL** via `DATABASE_URL`
- Browser dashboard UI for quick API interaction

## Role-Based Access

Supported roles:
- `admin`
- `doctor`
- `receptionist`

Permission model:
- `admin`: full system access
- `receptionist`: patient + appointment workflows, doctor assignment
- `doctor`: clinical workflows and medical records

## Core Features

1. Patient Management
- Create, list, get by ID, update, delete

2. Doctor Management
- Create, list, get by ID, update, delete
- Assign doctor to patient

3. Appointment System
- Book appointment
- View and update appointments
- Cancel or delete appointment

4. Medical Records
- Add medical records per patient
- View patient history
- Update and delete records (role-restricted)

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite / PostgreSQL
- Uvicorn

## Repository Structure

```text
app/
  core/
  database/
  models/
  routes/
  schemas/
  static/
  dependencies.py
  main.py
requirements.txt
Procfile
render.yaml
```

## Local Run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Local URLs:
- Dashboard: <http://127.0.0.1:8000/>
- Swagger: <http://127.0.0.1:8000/docs>

## Authentication Quick Start

Default seeded admin account:
- Username: `admin`
- Password: `admin123`

Auth endpoints:
- `POST /auth/login`
- `GET /auth/me`
- `POST /auth/register` (creates receptionist user)
- `POST /auth/users` (admin creates user with explicit role)

Use token as:
`Authorization: Bearer <access_token>`

## Sample API Requests

1. Login and get JWT token

```bash
curl -X POST "https://hospital-records-api.onrender.com/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

2. Create a patient (replace `<TOKEN>`)

```bash
curl -X POST "https://hospital-records-api.onrender.com/patients/" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Carter",
    "age": 38,
    "gender": "Male",
    "phone": "+1-555-001-9988",
    "address": "12 Lakeview Drive, Seattle"
  }'
```

3. Book an appointment (replace `<TOKEN>`)

```bash
curl -X POST "https://hospital-records-api.onrender.com/appointments/" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": 1,
    "doctor_id": 1,
    "appointment_date": "2026-03-25T10:30:00Z"
  }'
```

## Deployment Notes

- App uses `DATABASE_URL` in production.
- SQLite-only migration logic is guarded to avoid PostgreSQL startup errors.
- `SECRET_KEY` must be set in environment variables for production.

## Why This Project

This project demonstrates:
- API design and clean backend structure
- Authentication + authorization patterns
- SQL modeling and relational workflows
- Deployment readiness and production configuration
