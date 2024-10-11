from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from .forms import AttendanceForm, EventForm
from app.models import Member, Event, Attendance
from app import db
from datetime import datetime

# Define Blueprint
secretary_bp = Blueprint('secretary', __name__)

# Helper function to check user role
def is_secretary():
    return current_user.role.name.lower() == 'secretary'

# Secretary Dashboard
@secretary_bp.route('/dashboard')
@login_required
def dashboard():
    if not is_secretary():
        return redirect(url_for('main.unauthorized'))
    return render_template('secretary/dashboard.html', title="Secretary's Dashboard")

# Route to manage attendance
@secretary_bp.route('/attendance', methods=['GET', 'POST'])
@login_required
def attendance():
    if not is_secretary():
        return redirect(url_for('unauthorized'))
    
    form = AttendanceForm()
    
    # Populate member choices dynamically
    members = Member.query.all()
    form.members.choices = [(member.id, member.name) for member in members]

    if form.validate_on_submit():
        try:
            for member_id in form.members.data:
                attendance = Attendance(
                    member_id=member_id,
                    date=datetime.utcnow(),  # Use UTC for consistency
                    status=form.status.data
                )
                db.session.add(attendance)
            db.session.commit()
            flash('Attendance recorded successfully!', 'success')
            return redirect(url_for('secretary.attendance'))
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            flash(f'Error recording attendance: {str(e)}', 'danger')  # Provide error context

    return render_template('secretary/attendance.html', form=form, members=members, title="Manage Attendance")

# Route to record events
@secretary_bp.route('/record_event', methods=['GET', 'POST'])
@login_required
def record_event():
    if not is_secretary():
        return redirect(url_for('unauthorized'))
    
    form = EventForm()
    
    if form.validate_on_submit():
        try:
            event = Event(
                name=form.name.data,
                description=form.description.data,
                date=datetime.utcnow()  # Recording event date in UTC
            )
            db.session.add(event)
            db.session.commit()
            flash('Event recorded successfully!', 'success')
            return redirect(url_for('secretary.record_event'))
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            flash(f'Error recording event: {str(e)}', 'danger')  # Provide error context
    
    return render_template('secretary/record_event.html', form=form, title="Record Meeting Events")

@secretary_bp.route('/view_events')
@login_required
def view_events():
    if not is_secretary():
        return redirect(url_for('unauthorized'))
    
    events = Event.query.order_by(Event.date.desc()).all()  # Fetch all events, ordered by date
    return render_template('secretary/view_events.html', events=events, title="View Events")
