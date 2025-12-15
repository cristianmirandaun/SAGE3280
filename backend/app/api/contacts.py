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

@router.post("/", response_model=schemas.ContactRead)
def create_contact(payload: schemas.ContactCreate, db: Session = Depends(get_db)):
    patient = db.get(models.Patient, payload.patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    contact = models.Contact(**payload.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

@router.post("/attempt", response_model=schemas.ContactAttemptRead)
def log_attempt(payload: schemas.ContactAttemptCreate, db: Session = Depends(get_db)):
    patient = db.get(models.Patient, payload.patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    attempt = models.ContactAttempt(**payload.dict(), sent_at=datetime.utcnow())
    # update patient last contact if needed
    patient.last_contacted_at = datetime.utcnow()
    patient.is_contacted = True
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return attempt

@router.get("/", response_model=list[schemas.ContactRead])
def list_contacts(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(models.Contact).order_by(models.Contact.priority.desc()).offset(skip).limit(limit).all()
