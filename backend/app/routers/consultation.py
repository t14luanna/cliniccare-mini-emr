import sqlite3
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status

from app.database import get_db
from app.schemas import Consultation, ConsultationCreate

router = APIRouter(prefix="/consultation", tags=["consultation"])


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
            "INSERT INTO consultation (patient_name, notes, created_at) VALUES (?, ?, ?)",
            (payload.patient_name, payload.notes, created_at),
        )
        consultation_id = cursor.lastrowid
        db.executemany(
            "INSERT INTO consultation_diagnosis (consultation_id, diagnosis_code) VALUES (?, ?)",
            [(consultation_id, code) for code in payload.diagnosis_codes],
        )

    row = db.execute(
        "SELECT id, patient_name, notes, created_at FROM consultation WHERE id = ?",
        (consultation_id,),
    ).fetchone()
    return to_consultation(db, row)

