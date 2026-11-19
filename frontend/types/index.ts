export interface Diagnosis {
  code: string
  description: string
}

export interface Consultation {
  id: number
  patient_name: string
  notes: string
  created_at: string
  diagnoses: Diagnosis[]
}

export interface ConsultationCreate {
  patient_name: string
  notes: string
  diagnosis_codes: string[]
}
