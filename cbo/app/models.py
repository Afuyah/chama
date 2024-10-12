from datetime import datetime, timedelta
from flask_login import UserMixin
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    members = db.relationship('Member', backref='role', lazy=True)
    permissions = db.Column(db.String(200), nullable=True)  # For role-based permissions

    def __repr__(self):
        return f'<Role {self.name}>'

class Member(db.Model, UserMixin):
    __tablename__ = 'members'
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    residence = db.Column(db.String(100), nullable=False)
    county = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=True)
    join_date = db.Column(db.DateTime, default=datetime.utcnow)
    contributions = db.relationship('Contribution', backref='contributor', lazy='dynamic')
    fines = db.relationship('Fine', backref='fined_member', lazy='dynamic')
    attendance_records = db.relationship('Attendance', backref='attendee', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def total_contributions(self):
        return db.session.query(db.func.sum(Contribution.amount)).filter_by(member_id=self.id).scalar() or 0

    def total_fines(self):
        return db.session.query(db.func.sum(Fine.amount)).filter_by(member_id=self.id).scalar() or 0

class Contribution(db.Model):
    __tablename__ = 'contributions'
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

class FineType(db.Model):
    __tablename__ = 'fine_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<FineType {self.name} - {self.amount} KES>'

class Fine(db.Model):
    __tablename__ = 'fines'
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    fine_type_id = db.Column(db.Integer, db.ForeignKey('fine_types.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    reason = db.Column(db.String(200))

class Attendance(db.Model):
    __tablename__ = 'attendance'
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meetings.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Enum('Present', 'Late', 'Absent', name='attendance_status'), nullable=False)

class Meeting(db.Model):
    __tablename__ = 'meetings'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    minutes = db.Column(db.Text)
    attendance_records = db.relationship('Attendance', backref='meeting', lazy='dynamic')

    def __repr__(self):
        return f'<Meeting {self.date}>'

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    event_type = db.Column(db.String(50), nullable=False)  # Event types e.g. Public, Members Only

    def __repr__(self):
        return f'<Event {self.name} on {self.date}>'

class Report(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Report {self.title}>'
