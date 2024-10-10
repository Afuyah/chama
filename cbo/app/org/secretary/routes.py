from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from .forms import AttendanceForm, EventForm
from app.models import Member, Event, Attendance
from app import db
from datetime import datetime

# Define Blueprint
secretary_bp = Blueprint('secretary', __name__)

# Secretary Dashboard
@secretary_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'secretary':
        return redirect(url_for('unauthorized'))
    return render_template('secretary/dashboard.html', title="Secretary's Dashboard")

# Route to manage attendance
@secretary_bp.route('/attendance', methods=['GET', 'POST'])
@login_required
def attendance():
    if current_user.role != 'secretary':
        return redirect(url_for('unauthorized'))
    
    form = AttendanceForm()
    if form.validate_on_submit():
        for member_id in form.members.data:
            attendance = Attendance(
                member_id=member_id,
                date=datetime.now(),
                status=form.status.data
            )
            db.session.add(attendance)
        db.session.commit()
        flash('Attendance recorded successfully!', 'success')
        return redirect(url_for('secretary.attendance'))

    members = Member.query.all()
    return render_template('secretary/attendance.html', form=form, members=members, title="Manage Attendance")

# Route to record events
@secretary_bp.route('/record_event', methods=['GET', 'POST'])
@login_required
def record_event():
    if current_user.role != 'secretary':
        return redirect(url_for('unauthorized'))
    
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            name=form.name.data,
            description=form.description.data,
            date=datetime.now()
        )
        db.session.add(event)
        db.session.commit()
        flash('Event recorded successfully!', 'success')
        return redirect(url_for('secretary.record_event'))
    
    return render_template('secretary/record_event.html', form=form, title="Record Meeting Events")
