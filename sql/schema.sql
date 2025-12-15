-- DDL inicial para PostgreSQL (resumen)
CREATE TABLE patients (
  id serial PRIMARY KEY,
  document_type varchar(10),
  document_number varchar(64) NOT NULL UNIQUE,
  first_name varchar(128) NOT NULL,
  last_name varchar(128),
  birth_date date,
  phone varchar(32),
  email varchar(256),
  "group" varchar(2) NOT NULL,
  risk_level varchar(32),
  is_contacted boolean DEFAULT false,
  contact_status varchar(32),
  last_contacted_at timestamp,
  created_at timestamp DEFAULT now(),
  updated_at timestamp
);

CREATE INDEX idx_patients_document ON patients(document_number);
CREATE INDEX idx_patients_phone ON patients(phone);
CREATE INDEX idx_patients_group ON patients("group");
CREATE INDEX idx_patients_risk ON patients(risk_level);

CREATE TABLE contacts (
  id serial PRIMARY KEY,
  patient_id integer REFERENCES patients(id),
  contact_reason varchar(256) NOT NULL,
  contact_type varchar(64) NOT NULL,
  priority integer DEFAULT 0,
  scheduled_at timestamp,
  sent_at timestamp,
  status varchar(32) DEFAULT 'pending',
  metadata jsonb,
  created_at timestamp DEFAULT now()
);
CREATE INDEX idx_contacts_patient ON contacts(patient_id);
CREATE INDEX idx_contacts_status ON contacts(status);

CREATE TABLE contact_attempts (
  id serial PRIMARY KEY,
  contact_id integer REFERENCES contacts(id),
  patient_id integer REFERENCES patients(id) NOT NULL,
  attempt_number integer NOT NULL DEFAULT 1,
  message text,
  response text,
  response_code varchar(64),
  sent_at timestamp DEFAULT now(),
  response_at timestamp,
  metadata jsonb
);
CREATE INDEX idx_attempts_patient ON contact_attempts(patient_id);

CREATE TABLE appointments (
  id serial PRIMARY KEY,
  patient_id integer REFERENCES patients(id) NOT NULL,
  appointment_date timestamp NOT NULL,
  appointment_type varchar(128),
  status varchar(32) DEFAULT 'scheduled',
  created_by varchar(128),
  created_at timestamp DEFAULT now(),
  metadata jsonb
);
CREATE INDEX idx_appointments_patient ON appointments(patient_id);
CREATE INDEX idx_appointments_date ON appointments(appointment_date);
