from flask_login import UserMixin
from .extensions import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)


class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    specialization_id = db.Column(db.Integer, db.ForeignKey('specialization.id'), nullable=False)
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)
    specialization = db.relationship('Specialization', foreign_keys=[specialization_id],backref='doctor', lazy=True)
    user = db.relationship('User', backref='doctor', uselist=False)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    appointments = db.relationship('Appointment', backref='patient', lazy=True)
    user = db.relationship('User', backref='patient', uselist=False)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    procedure_id = db.Column(db.Integer, db.ForeignKey('procedure.id'), nullable=False)
    appointment_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='scheduled') #completed, cancel

    @staticmethod
    def get_time_slots(doctor_id, date):
        appointments = Appointment.query.filter(
            Appointment.doctor_id == doctor_id,
            db.func.date(Appointment.appointment_time) == date
        ).all()
        return [a.appointment_time.strftime('%H:%M') for a in appointments]

class Specialization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    procedures = db.relationship('Procedure', backref='specialization', lazy=True)

class Procedure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialization_id = db.Column(db.Integer, db.ForeignKey('specialization.id'), nullable=False)
    appointments = db.relationship('Appointment', backref='procedure', lazy=True)