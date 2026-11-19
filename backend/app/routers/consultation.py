import sqlite3
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.auth import get_current_doctor
from app.database import get_db
from app.schemas import Consultation, ConsultationCreate

router = APIRouter(
    prefix="/consultation",
    tags=["consultation"],
    dependencies=[Depends(get_current_doctor)],
)

SELECT_CONSULTATION = """
    SELECT c.id, c.patient_name, c.notes, c.created_at, d.full_name AS doctor_name
    FROM consultation c
    JOIN doctor d ON d.id = c.doctor_id
"""


def get_diagnoses(db: sqlite3.Connection, consultation_id: int) -> list[dict]:
    rows = db.execute(
        """
        SELECT d.code, d.description
        FROM consultation_diagnosis cd
        JOIN diagnosis d ON d.code = cd.diagnosis_code
        WHERE cd.consultation_id = ?
        ORDER BY d.code
        """,
        (consultation_id,),
    ).fetchall()
    return [dict(row) for row in rows]


def to_consultation(db: sqlite3.Connection, row: sqlite3.Row) -> dict:
    consultation = dict(row)
    consultation["diagnoses"] = get_diagnoses(db, row["id"])
    return consultation


@router.post("", response_model=Consultation, status_code=status.HTTP_201_CREATED)
def create_consultation(
    payload: ConsultationCreate,
    db: sqlite3.Connection = Depends(get_db),
    doctor: dict = Depends(get_current_doctor),
):
    placeholders = ",".join("?" for _ in payload.diagnosis_codes)
    found = db.execute(
        f"SELECT code FROM diagnosis WHERE code IN ({placeholders})",
        payload.diagnosis_codes,
    ).fetchall()
    unknown = set(payload.diagnosis_codes) - {row["code"] for row in found}
    if unknown:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown diagnosis codes: {', '.join(sorted(unknown))}",
        )

    # commits at the end, rolls back if something fails
    created_at = datetime.now(timezone.utc).isoformat()
    with db:
        cursor = db.execute(
            """
            INSERT INTO consultation (patient_name, notes, created_at, doctor_id)
            VALUES (?, ?, ?, ?)
            """,
            (payload.patient_name, payload.notes, created_at, doctor["id"]),
        )
        consultation_id = cursor.lastrowid
        db.executemany(
            "INSERT INTO consultation_diagnosis (consultation_id, diagnosis_code) VALUES (?, ?)",
            [(consultation_id, code) for code in payload.diagnosis_codes],
        )

    row = db.execute(
        f"{SELECT_CONSULTATION} WHERE c.id = ?",
        (consultation_id,),
    ).fetchone()
    return to_consultation(db, row)


@router.get("", response_model=list[Consultation])
def list_consultations(
    patient: str | None = Query(None, max_length=100, description="Part of the patient name"),
    diagnosis_code: str | None = Query(None, max_length=20, description="Exact ICD-10 code"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: sqlite3.Connection = Depends(get_db),
):
    sql = f"{SELECT_CONSULTATION} WHERE 1 = 1"
    params: list = []

    if patient and patient.strip():
        sql += " AND c.patient_name LIKE ?"
        params.append(f"%{patient.strip()}%")

    if diagnosis_code and diagnosis_code.strip():
        sql += """ AND c.id IN (
            SELECT consultation_id FROM consultation_diagnosis WHERE diagnosis_code = ?
        )"""
        params.append(diagnosis_code.strip().upper())

    sql += " ORDER BY c.created_at DESC, c.id DESC"
    sql += " LIMIT ? OFFSET ?"
    params += [limit, offset]

    rows = db.execute(sql, params).fetchall()
    return [to_consultation(db, row) for row in rows]
