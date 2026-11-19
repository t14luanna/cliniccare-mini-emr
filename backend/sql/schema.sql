-- ICD-10 codes, data in seed_diagnosis.sql
CREATE TABLE IF NOT EXISTS diagnosis (
    code        TEXT PRIMARY KEY,
    description TEXT NOT NULL
);

-- one row per visit
CREATE TABLE IF NOT EXISTS consultation (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_name TEXT NOT NULL,
    notes        TEXT NOT NULL,
    created_at   TEXT NOT NULL
);

-- many-to-many between consultation and diagnosis
CREATE TABLE IF NOT EXISTS consultation_diagnosis (
    consultation_id INTEGER NOT NULL REFERENCES consultation(id) ON DELETE CASCADE,
    diagnosis_code  TEXT    NOT NULL REFERENCES diagnosis(code),
    PRIMARY KEY (consultation_id, diagnosis_code)
);

CREATE INDEX IF NOT EXISTS idx_consultation_patient_name ON consultation(patient_name);
CREATE INDEX IF NOT EXISTS idx_consultation_diagnosis_code ON consultation_diagnosis(diagnosis_code);
