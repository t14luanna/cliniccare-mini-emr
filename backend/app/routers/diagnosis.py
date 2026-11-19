import sqlite3

from fastapi import APIRouter, Depends, Query

from app.auth import get_current_doctor
from app.database import get_db
from app.schemas import Diagnosis

router = APIRouter(
    prefix="/diagnosis",
    tags=["diagnosis"],
    dependencies=[Depends(get_current_doctor)],
)


@router.get("", response_model=list[Diagnosis])
def search_diagnosis(
    search: str = Query("", max_length=100, description="Code or words in the description"),
    limit: int = Query(20, ge=1, le=100),
    db: sqlite3.Connection = Depends(get_db),
):
    term = search.strip()
    # code starts with the term, or description contains it
    rows = db.execute(
        """
        SELECT code, description FROM diagnosis
        WHERE code LIKE ? OR description LIKE ?
        ORDER BY code
        LIMIT ?
        """,
        (f"{term}%", f"%{term}%", limit),
    ).fetchall()
    return [dict(row) for row in rows]
