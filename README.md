# ClinicCare Mini EMR

Small web app for doctors to write consultation notes with ICD-10 diagnosis codes.

- Search ICD-10 codes (100 codes seeded from icd10data.com)
- Create a consultation note with one or more diagnosis codes
- List past consultations (with pagination)
- Search consultations by patient name or diagnosis code
- Login for doctors with JWT

**Backend:** FastAPI, Pydantic, SQLite
**Frontend:** Nuxt 3

## Run locally

Backend (Python 3.10+):

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload --port 8000
```

The SQLite file `backend/cliniccare.db` is created on first start from `sql/schema.sql` and `sql/seed_diagnosis.sql`.
Swagger docs: http://localhost:8000/docs

Tests:

```bash
cd backend
pytest
```

Frontend (Node 18+):

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000 and log in with **doctor / doctor123**.

### Config

All optional, defaults work for local dev.

| Variable | Default | |
|---|---|---|
| `DB_PATH` | `backend/cliniccare.db` | SQLite file |
| `JWT_SECRET` | `dev-secret-change-me` | **must** be set outside local dev |
| `CORS_ORIGINS` | `http://localhost:3000` | comma separated |
| `DEMO_DOCTOR_USERNAME` / `DEMO_DOCTOR_PASSWORD` | `doctor` / `doctor123` | demo account created on startup |
| `NUXT_PUBLIC_API_BASE` | `http://localhost:8000` | frontend → API URL |

## API

All endpoints except `/auth/login` need `Authorization: Bearer <token>`.

| Method | Path | |
|---|---|---|
| POST | `/auth/login` | `{ username, password }` → token |
| GET | `/auth/me` | current doctor |
| GET | `/diagnosis?search=` | search by code or description |
| POST | `/consultation` | `{ patient_name, notes, diagnosis_codes }` |
| GET | `/consultation?patient=&diagnosis_code=&limit=&offset=` | list / search, newest first |

Errors: `422` invalid input, `400` unknown diagnosis code, `401` not logged in.

## Assumptions

- A patient is identified by name only (the brief has no patient record). Search by name is a "contains" match.
- Diagnosis search matches the start of a code (`E11` → `E11.9`) or any part of the description.
- Search by diagnosis is an exact code match, case-insensitive.
- Consultations are visible to every logged-in doctor (small clinic, no per-doctor access rules).

## Notes

- I used plain `sqlite3` with SQL files instead of an ORM because there are only a few tables.
- `consultation_diagnosis` is a many-to-many table (one note has many codes, one code is used in many notes).
- A consultation and its codes are saved in one transaction.
- The frontend runs as an SPA (`ssr: false`) since it's an internal tool behind a login.

## Before going to production

- Set a real `JWT_SECRET` and restrict `CORS_ORIGINS`
- Remove the demo account, add proper doctor management
- PostgreSQL + Alembic migrations instead of a SQLite file and `CREATE TABLE IF NOT EXISTS`
- Token in an httpOnly cookie set by the backend, rate limiting on `/auth/login`
- Audit log of who read/changed which note (medical data)
- HTTPS, backups, logging/monitoring

## Next steps

- Patient table (ID, date of birth) instead of only a name
- Edit consultations
- Total count in the list API for "page X of Y"
- Frontend tests
