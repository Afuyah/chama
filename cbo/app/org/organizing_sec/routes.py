from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from .forms import AttendanceForm
from app.models import Attendance, Member
from app import db
from datetime import datetime

# Define Blueprint
organizing_secretary_bp = Blueprint('organizing_secretary', __name__)

# Organizing Secretary Dashboard
@organizing_secretary_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'organizing_secretary':
        return redirect(url_for('unauthorized'))

    attendances = Attendance.query.order_by(Attendance.date.desc()).limit(10).all()
    return render_template('organizing_secretary/dashboard.html', attendances=attendances, title="Organizing Secretary's Dashboard")

# Record attendance
@organizing_secretary_bp.route('/record_attendance', methods=['GET', 'POST'])
@login_required
def record_attendance():
    if current_user.role != 'organizing_secretary':
        return redirect(url_for('unauthorized'))

    form = AttendanceForm()
    if form.validate_on_submit():
        attendance = Attendance(
            member_id=form.member.data,
            status=form.status.data,
            fine_amount=form.fine_amount.data if form.status.data in ['Late', 'Absent'] else 0,
            date=datetime.now()
        )
        db.session.add(attendance)
        db.session.commit()
        flash('Attendance recorded successfully!', 'success')
        return redirect(url_for('organizing_secretary.record_attendance'))

    members = Member.query.all()
    return render_template('organizing_secretary/record_attendance.html', form=form, members=members, title="Record Attendance")

# View attendance records
@organizing_secretary_bp.route('/view_attendance')
@login_required
def view_attendance():
    if current_user.role != 'organizing_secretary':
        return redirect(url_for('unauthorized'))

    attendances = Attendance.query.order_by(Attendance.date.desc()).all()
    return render_template('organizing_secretary/view_attendance.html', attendances=attendances, title="View Attendance Records")
