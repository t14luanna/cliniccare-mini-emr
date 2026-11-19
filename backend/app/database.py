import os
import sqlite3
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
SQL_DIR = BACKEND_DIR / "sql"


def get_db_path() -> str:
    # read each time so tests can use a temp db
    return os.getenv("DB_PATH", str(BACKEND_DIR / "cliniccare.db"))


def get_connection() -> sqlite3.Connection:
    # FastAPI may run the endpoint in another thread
    conn = sqlite3.connect(get_db_path(), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def get_db():
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()


def init_db() -> None:
    conn = get_connection()
    try:
        conn.executescript((SQL_DIR / "schema.sql").read_text())
        conn.executescript((SQL_DIR / "seed_diagnosis.sql").read_text())
        create_demo_doctor(conn)
        conn.commit()
    finally:
        conn.close()


def create_demo_doctor(conn: sqlite3.Connection) -> None:
    from app.auth import hash_password  # circular import otherwise

    username = os.getenv("DEMO_DOCTOR_USERNAME", "doctor")
    password = os.getenv("DEMO_DOCTOR_PASSWORD", "doctor123")
    exists = conn.execute("SELECT 1 FROM doctor WHERE username = ?", (username,)).fetchone()
    if not exists:
        conn.execute(
            "INSERT INTO doctor (username, full_name, password_hash) VALUES (?, ?, ?)",
            (username, "Dr. Demo", hash_password(password)),
        )
