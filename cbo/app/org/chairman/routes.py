from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .forms import AddMemberForm, ScheduleMeetingForm, ManageEventForm
from app.models import Member, Meeting, Contribution, Event, Attendance
from app import db

# Define Blueprint
chairman_bp = Blueprint('chairman', __name__)

# Chairman Dashboard
@chairman_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role.name.lower() != 'chairman':
        return redirect(url_for('main.unauthorized'))
    
    total_members = Member.query.count()
    total_contributions = sum(contribution.amount for contribution in Contribution.query.all())
    
    return render_template('chairman/dashboard.html', title="Chairman's Dashboard", total_members=total_members, total_contributions=total_contributions)

# Member Management
@chairman_bp.route('/add_member', methods=['GET', 'POST'])
@login_required
def add_member():
    if current_user.role.name.lower() != 'chairman':
        return redirect(url_for('main.unauthorized'))

    form = AddMemberForm()
    if form.validate_on_submit():
        new_member = Member(
            name=form.name.data,
            phone_number=form.phone.data,
            residence=form.residence.data,
            county=form.county.data,
            gender=form.gender.data,
            age=form.age.data
        )

        new_member.set_password(form.national_id.data)
        try:
            db.session.add(new_member)
            db.session.commit()
            flash('New member added successfully!', 'success')
            return redirect(url_for('chairman.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding new member: {str(e)}', 'danger')

    return render_template('chairman/add_member.html', form=form, title="Add Member")

@chairman_bp.route('/view_members', methods=['GET'])
@login_required
def view_members():
    if current_user.role.name.lower() != 'chairman':
        return redirect(url_for('main.unauthorized'))

    members = Member.query.all()
    return render_template('chairman/view_members.html', members=members)

@chairman_bp.route('/edit_member/<int:member_id>', methods=['GET', 'POST'])
@login_required
def edit_member(member_id):
    if current_user.role.name.lower() != 'chairman':
        return redirect(url_for('main.unauthorized'))

    member = Member.query.get_or_404(member_id)
    form = AddMemberForm(obj=member)

    if form.validate_on_submit():
        member.name = form.name.data
        member.phone_number = form.phone.data
        member.residence = form.residence.data
        member.county = form.county.data
        member.gender = form.gender.data
        member.age = form.age.data

        try:
            db.session.commit()
            flash('Member updated successfully!', 'success')
            return redirect(url_for('chairman.view_members'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating member: {str(e)}', 'danger')

    return render_template('chairman/edit_member.html', form=form, title="Edit Member")

@chairman_bp.route('/delete_member/<int:member_id>', methods=['POST'])
@login_required
def delete_member(member_id):
    if current_user.role.name.lower() != 'chairman':
        return redirect(url_for('main.unauthorized'))

    member = Member.query.get_or_404(member_id)

    try:
        db.session.delete(member)
        db.session.commit()
        flash('Member deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting member: {str(e)}', 'danger')

    return redirect(url_for('chairman.view_members'))

# Meeting Management
@chairman_bp.route('/schedule_meeting', methods=['GET', 'POST'])
@login_required
def schedule_meeting():
    if current_user.role.name.lower() != 'chairman':
        return redirect(url_for('main.unauthorized'))

    form = ScheduleMeetingForm()
    if form.validate_on_submit():
        new_meeting = Meeting(
            date=form.date.data,
            minutes=form.minutes.data
        )

        try:
            db.session.add(new_meeting)
            db.session.commit()
            flash('Meeting scheduled successfully!', 'success')
            return redirect(url_for('chairman.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error scheduling meeting: {str(e)}', 'danger')

    return render_template('chairman/schedule_meeting.html', form=form, title="Schedule Meeting")

@chairman_bp.route('/view_meetings', methods=['GET'])
@login_required
def view_meetings():
    if current_user.role.name.lower() != 'chairman':
        return redirect(url_for('main.unauthorized'))

    meetings = Meeting.query.all()
    return render_template('chairman/view_meetings.html', meetings=meetings)

@chairman_bp.route('/meeting_attendance/<int:meeting_id>', methods=['GET'])
@login_required
def meeting_attendance(meeting_id):
    if current_user.role.name.lower() != 'chairman':
        return redirect(url_for('main.unauthorized'))

    meeting = Meeting.query.get_or_404(meeting_id)
    attendance_records = Attendance.query.filter_by(meeting_id=meeting.id).all()
    return render_template('chairman/meeting_attendance.html', meeting=meeting, attendance_records=attendance_records)

# Event Management
@chairman_bp.route('/manage_events', methods=['GET', 'POST'])
@login_required
def manage_events():
    if current_user.role.name.lower() != 'chairman':
        return redirect(url_for('main.unauthorized'))

    form = ManageEventForm()
    if form.validate_on_submit():
        new_event = Event(
            name=form.name.data,
            description=form.description.data,
            date=form.date.data
        )

        try:
            db.session.add(new_event)
            db.session.commit()
            flash('Event created successfully!', 'success')
            return redirect(url_for('chairman.manage_events'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating event: {str(e)}', 'danger')

    events = Event.query.all()
    return render_template('chairman/manage_events.html', form=form, events=events, title="Manage Events")

@chairman_bp.route('/delete_event/<int:event_id>', methods=['POST'])
@login_required
def delete_event(event_id):
    if current_user.role.name.lower() != 'chairman':
        return redirect(url_for('main.unauthorized'))

    event = Event.query.get_or_404(event_id)

    try:
        db.session.delete(event)
        db.session.commit()
        flash('Event deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting event: {str(e)}', 'danger')

    return redirect(url_for('chairman.manage_events'))

# Financial Oversight
@chairman_bp.route('/view_contributions', methods=['GET'])
@login_required
def view_contributions():
    if current_user.role.name.lower() != 'chairman':
        return redirect(url_for('main.unauthorized'))

    contributions = Contribution.query.all()
    return render_template('chairman/view_contributions.html', contributions=contributions)

# Communication
@chairman_bp.route('/send_announcement', methods=['POST'])
@login_required
def send_announcement():
    if current_user.role.name.lower() != 'chairman':
        return redirect(url_for('main.unauthorized'))

    announcement = request.form.get('announcement')
    # Logic to send announcement to members (e.g., email or in-app notifications)

    flash('Announcement sent successfully!', 'success')
    return redirect(url_for('chairman.dashboard'))

# Role Management
@chairman_bp.route('/assign_role/<int:member_id>', methods=['POST'])
@login_required
def assign_role(member_id):
    if current_user.role.name.lower() != 'chairman':
        return redirect(url_for('main.unauthorized'))

    member = Member.query.get_or_404(member_id)
    new_role = request.form.get('role')  # Assume this comes from a select form

    # Logic to assign new role to member
    # Update member.role_id based on new_role selection
    flash('Role assigned successfully!', 'success')
    return redirect(url_for('chairman.view_members'))

@chairman_bp.route('/generate_report', methods=['GET', 'POST'])
@login_required
def generate_report():
    if current_user.role.name.lower() != 'chairman':
        return redirect(url_for('main.unauthorized'))

    form = ReportForm()
    if form.validate_on_submit():
        report_type = form.report_type.data
        start_date = form.start_date.data
        end_date = form.end_date.data

        if report_type == 'contribution':
            contributions = Contribution.query.filter(Contribution.date.between(start_date, end_date)).all()
            return render_template('reports/contribution_report.html', contributions=contributions)

        elif report_type == 'attendance':
            attendance_records = Attendance.query.filter(Attendance.date.between(start_date, end_date)).all()
            return render_template('reports/attendance_report.html', attendance=attendance_records)

        elif report_type == 'fine':
            fines = Fine.query.filter(Fine.date.between(start_date, end_date)).all()
            return render_template('reports/fine_report.html', fines=fines)

        elif report_type == 'event':
            events = Event.query.filter(Event.date.between(start_date, end_date)).all()
            return render_template('reports/event_report.html', events=events)

    return render_template('reports/generate_report.html', form=form, title="Generate Report")
