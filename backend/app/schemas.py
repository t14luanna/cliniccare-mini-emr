from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class Diagnosis(BaseModel):
    code: str
    description: str


class ConsultationCreate(BaseModel):
    patient_name: str = Field(min_length=2, max_length=100)
    notes: str = Field(min_length=1, max_length=5000)
    diagnosis_codes: list[str] = Field(min_length=1, max_length=20)

    @field_validator("patient_name", "notes", mode="before")
    @classmethod
    def strip_text(cls, value):
        # strip first so "   " fails min_length
        return value.strip() if isinstance(value, str) else value

    @field_validator("diagnosis_codes")
    @classmethod
    def clean_codes(cls, codes: list[str]) -> list[str]:
        cleaned = [code.strip().upper() for code in codes if code.strip()]
        if not cleaned:
            raise ValueError("At least one diagnosis code is required")
        return list(dict.fromkeys(cleaned))


class Consultation(BaseModel):
    id: int
    patient_name: str
    notes: str
    created_at: datetime
    diagnoses: list[Diagnosis]
