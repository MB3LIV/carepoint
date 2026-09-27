from pkg import db
from datetime import datetime


class Specialty(db.Model):
    __tablename__ = 'Specialty'

    id = db.Column(db.Integer,primary_key = True, autoincrement = True)
    name = db.Column(db.String(200), nullable = False, index = True,unique = True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default = datetime.utcnow)
    doctors = db.relationship("Doctor", backref = 'specialty')


class Doctor(db.Model):
    __tablename__ = 'Doctors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(200), nullable=False, index=True)
    last_name = db.Column(db.String(200), nullable=False, index=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    specialty_id = db.Column(db.Integer, db.ForeignKey("Specialty.id"), nullable=False)
    availability = db.Column(db.Boolean, default=True, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    licence_no = db.Column(db.String(50), unique=True, nullable=False)
    consultation_fee = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)   # <-- NEW
    created_at = db.Column(db.DateTime, default=datetime.utcnow)



class Appointment(db.Model):
    __tablename__ = 'Appointments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # patient_id = db.Column(db.Integer, db.ForeignKey("Patients.id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("Doctors.id"), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)
    reason = db.Column(db.String(255), nullable=True)

    status = db.Column(
        db.Enum('Pending', 'Accepted', 'Rejected', 'Cancelled', 'Completed', name='appointment_status'),
        default='Pending',
        nullable=False
    )
    # patient =  db.relationship("Patient", backref="appointments")
    doctor =  db.relationship("Doctor", backref="appointments")