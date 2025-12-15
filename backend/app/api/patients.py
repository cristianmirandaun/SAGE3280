from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.PatientRead)
def create_patient(payload: schemas.PatientCreate, db: Session = Depends(get_db)):
    p = db.query(models.Patient).filter(models.Patient.document_number == payload.document_number).first()
    if p:
        raise HTTPException(status_code=400, detail="Paciente ya existe con ese documento")
    patient = models.Patient(**payload.dict())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

@router.get("/{patient_id}", response_model=schemas.PatientRead)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.get(models.Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return patient

@router.get("/", response_model=list[schemas.PatientRead])
def list_patients(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(models.Patient).offset(skip).limit(limit).all()
