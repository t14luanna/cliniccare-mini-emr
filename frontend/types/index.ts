export interface Diagnosis {
  code: string
  description: string
}

export interface Consultation {
  id: number
  patient_name: string
  notes: string
  created_at: string
  doctor_name: string
  diagnoses: Diagnosis[]
}

export interface ConsultationCreate {
  patient_name: string
  notes: string
  diagnosis_codes: string[]
}

export interface LoginResponse {
  access_token: string
  token_type: string
  doctor: {
    username: string
    full_name: string
  }
}
