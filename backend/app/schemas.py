from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date

class PatientBase(BaseModel):
    document_type: Optional[str]
    document_number: str
    first_name: str
    last_name: Optional[str]
    birth_date: Optional[date]
    phone: Optional[str]
    email: Optional[str]
    group: str
    risk_level: Optional[str]

class PatientCreate(PatientBase):
    pass

class PatientRead(PatientBase):
    id: int
    is_contacted: Optional[bool]
    contact_status: Optional[str]
    last_contacted_at: Optional[datetime]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True

class ContactCreate(BaseModel):
    patient_id: int
    contact_reason: str
    contact_type: str
    scheduled_at: Optional[datetime]
    priority: Optional[int] = 0
    metadata: Optional[dict] = None

class ContactRead(ContactCreate):
    id: int
    status: str
    sent_at: Optional[datetime]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True

class ContactAttemptCreate(BaseModel):
    contact_id: Optional[int]
    patient_id: int
    attempt_number: int
    message: Optional[str]
    response: Optional[str]
    response_code: Optional[str]

class ContactAttemptRead(ContactAttemptCreate):
    id: int
    sent_at: Optional[datetime]
    response_at: Optional[datetime]

    class Config:
        orm_mode = True

class AppointmentCreate(BaseModel):
    patient_id: int
    appointment_date: datetime
    appointment_type: Optional[str] = None

class AppointmentRead(AppointmentCreate):
    id: int
    status: str
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
