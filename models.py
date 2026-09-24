from app import db
from datetime import datetime


class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    specialization = db.Column(db.String(120), nullable=False)
    available = db.Column(db.Boolean, default=True)

    appointments = db.relationship("Appointment", backref="doctor", lazy=True)


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10))
    contact = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # vitals used by the ML risk model
    resting_bp = db.Column(db.Float)
    cholesterol = db.Column(db.Float)
    bmi = db.Column(db.Float)
    max_heart_rate = db.Column(db.Float)
    smoker = db.Column(db.Boolean, default=False)
    exercise_hours_week = db.Column(db.Float)
    family_history = db.Column(db.Boolean, default=False)

    # last computed risk
    risk_score = db.Column(db.Float)
    risk_label = db.Column(db.String(20))

    appointments = db.relationship("Appointment", backref="patient", lazy=True)


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.id"), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default="Scheduled")
    reason = db.Column(db.String(255))
