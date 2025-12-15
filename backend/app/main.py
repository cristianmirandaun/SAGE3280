from fastapi import FastAPI
from .database import engine, Base
from .api import patients, contacts, appointments

# Crear tablas si no existen (solo para desarrollo)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SAGE3280 - API base")

app.include_router(patients.router, prefix="/patients", tags=["patients"]) 
app.include_router(contacts.router, prefix="/contacts", tags=["contacts"]) 
app.include_router(appointments.router, prefix="/appointments", tags=["appointments"]) 
