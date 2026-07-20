from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, date

db = SQLAlchemy()

class Employee(UserMixin, db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='employee') # 'employee' or 'admin'
    
    attendances = db.relationship('Attendance', backref='employee', lazy=True)
    visits = db.relationship('ClientVisit', backref='employee', lazy=True)

class Attendance(db.Model):
    __tablename__ = 'attendance'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)
    check_in = db.Column(db.DateTime, nullable=True)
    check_out = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='Present') # Present, Half Day, Absent

class ClientVisit(db.Model):
    __tablename__ = 'client_visit'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    client_name = db.Column(db.String(100), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    visit_date = db.Column(db.Date, nullable=False, default=date.today)
    purpose = db.Column(db.String(200), nullable=False)
    meeting_notes = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='Pending') # Pending, Completed, Cancelled
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
