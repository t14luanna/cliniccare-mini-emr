from pydantic import BaseModel


class Diagnosis(BaseModel):
    code: str
    description: str
