# Hospital Records API

REST API for managing patients, doctors, appointments, and medical records.

Stack:
- FastAPI
- SQLAlchemy ORM
- SQLite
- JWT authentication

Includes:
- Role-based access (`admin`, `doctor`, `receptionist`)
- Swagger docs at `/docs`
- Lightweight web dashboard at `/`

## Project Layout

```text
app/
  core/
    config.py
    security.py
  database/
    db.py
  models/
    appointment.py
    doctor.py
    doctor_patient_assignment.py
    medical_record.py
    patient.py
    user.py
  routes/
    appointments.py
    auth.py
    doctors.py
    medical_records.py
    patients.py
  schemas/
    appointment.py
    auth.py
    doctor.py
    medical_record.py
    patient.py
  static/
    index.html
  dependencies.py
  main.py
requirements.txt
```

## Quick Start (Windows / PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Open:
- Dashboard: <http://127.0.0.1:8000/>
- Swagger docs: <http://127.0.0.1:8000/docs>
- Health check: <http://127.0.0.1:8000/health>

## Authentication

Default admin (seeded on startup):
- Username: `admin`
- Password: `admin123`
- Role: `admin`

Auth endpoints:
- `POST /auth/login` -> returns JWT
- `GET /auth/me` -> current authenticated user
- `POST /auth/register` -> public signup (creates `receptionist`)
- `POST /auth/users` -> admin-only user creation with explicit role

For protected endpoints, send:
`Authorization: Bearer <access_token>`

## Roles and Permissions

- `admin`
  - Full access
  - Can create staff users with roles
  - Can perform destructive operations
- `receptionist`
  - Patient workflows
  - Appointment workflows
  - Doctor-patient assignment
- `doctor`
  - View patient/doctor/appointment data
  - Create and update medical records

## Main API Groups

- `/patients`
- `/doctors`
- `/appointments`
- `/medical-records`
- `/auth`

## Example Workflow

1. Login as admin (`/auth/login`)
2. Create doctors (`POST /doctors/`)
3. Create patients (`POST /patients/`)
4. Assign doctor to patient (`POST /doctors/assign`)
5. Book appointment (`POST /appointments/`)
6. Add medical record (`POST /medical-records/`)
7. Review patient history (`GET /medical-records/patient/{patient_id}`)

## Notes

- Database file is created automatically: `hospital.db`
- Existing databases are upgraded at startup to include `users.role` if missing
- If you change auth or schema models, restart the server

## Troubleshooting

- If port `8000` is already in use, stop the old process and restart Uvicorn.
- If requests return `401`, check your token.
- If requests return `403`, your role does not have access to that endpoint.
