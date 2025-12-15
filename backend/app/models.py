from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, Enum, Text, ForeignKey, JSON, func, Index
from sqlalchemy.orm import relationship
from .database import Base
import enum

class PatientGroup(str, enum.Enum):
    A = "A"  # Preventive - RIAS
    B = "B"  # Chronic
    C = "C"  # General consultation

class ContactStatus(str, enum.Enum):
    pending = "pending"
    sent = "sent"
    confirmed = "confirmed"
    reprogrammed = "reprogrammed"
    rejected = "rejected"
    no_response = "no_response"

class AppointmentStatus(str, enum.Enum):
    scheduled = "scheduled"
    attended = "attended"
    missed = "missed"
    cancelled = "cancelled"

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True)
    document_type = Column(String(10), nullable=True)
    document_number = Column(String(64), nullable=False, unique=True, index=True)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=True)
    birth_date = Column(Date, nullable=True)
    phone = Column(String(32), nullable=True, index=True)
    email = Column(String(256), nullable=True)
    group = Column(Enum(PatientGroup), nullable=False, index=True)
    risk_level = Column(String(32), nullable=True, index=True)  # low/medium/high or more granular
    is_contacted = Column(Boolean, default=False, index=True)
    contact_status = Column(String(32), nullable=True, index=True)
    last_contacted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    contacts = relationship("Contact", back_populates="patient")
    appointments = relationship("Appointment", back_populates="patient")
    attempts = relationship("ContactAttempt", back_populates="patient")

Index("ix_patients_doc_phone", Patient.document_number, Patient.phone)

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    contact_reason = Column(String(256), nullable=False)
    contact_type = Column(String(64), nullable=False)  # e.g., "whatsapp_automatic" or "manual"
    priority = Column(Integer, default=0, index=True)
    scheduled_at = Column(DateTime, nullable=True)
    sent_at = Column(DateTime, nullable=True)
    status = Column(Enum(ContactStatus), default=ContactStatus.pending, index=True)
    metadata = Column(JSON, nullable=True)  # store extra data (language, template, program)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    patient = relationship("Patient", back_populates="contacts")
    attempts = relationship("ContactAttempt", back_populates="contact")

class ContactAttempt(Base):
    __tablename__ = "contact_attempts"
    id = Column(Integer, primary_key=True)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    attempt_number = Column(Integer, nullable=False, default=1)
    message = Column(Text, nullable=True)
    response = Column(Text, nullable=True)
    response_code = Column(String(64), nullable=True)  # normalized: confirm,reprogram,deny,unknown
    sent_at = Column(DateTime(timezone=True), server_default=func.now())
    response_at = Column(DateTime, nullable=True)
    metadata = Column(JSON, nullable=True)

    contact = relationship("Contact", back_populates="attempts")
    patient = relationship("Patient", back_populates="attempts")

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    appointment_date = Column(DateTime, nullable=False, index=True)
    appointment_type = Column(String(128), nullable=True)  # e.g., "control_hipertension"
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.scheduled, index=True)
    created_by = Column(String(128), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    metadata = Column(JSON, nullable=True)

    patient = relationship("Patient", back_populates="appointments")

class Parameter(Base):
    __tablename__ = "parameters"
    id = Column(Integer, primary_key=True)
    key = Column(String(128), nullable=False, unique=True, index=True)
    value = Column(JSON, nullable=False)
    description = Column(Text, nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
