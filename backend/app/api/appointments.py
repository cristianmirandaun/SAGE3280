from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import SessionLocal
from datetime import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.AppointmentRead)
def create_appointment(payload: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    patient = db.get(models.Patient, payload.patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    appt = models.Appointment(**payload.dict())
    db.add(appt)
    db.commit()
    db.refresh(appt)
    return appt

@router.get("/patient/{patient_id}", response_model=list[schemas.AppointmentRead])
def list_appointments_for_patient(patient_id: int, skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(models.Appointment).filter(models.Appointment.patient_id == patient_id).order_by(models.Appointment.appointment_date.desc()).offset(skip).limit(limit).all()
