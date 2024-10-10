from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Contribution, Attendance
from app import db

# Define Blueprint
patron_bp = Blueprint('patron', __name__)

# Patron Dashboard
@patron_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'patron':
        return redirect(url_for('unauthorized'))

    # Summarize contributions and fines for each member
    contributions_summary = db.session.query(
        Member.name,
        db.func.sum(Contribution.amount).label('total_contributions'),
        db.func.sum(Attendance.fine_amount).label('total_fines')
    ).join(Contribution, Member.id == Contribution.member_id, isouter=True).join(Attendance, Member.id == Attendance.member_id, isouter=True).group_by(Member.id).all()

    return render_template('patron/dashboard.html', contributions_summary=contributions_summary, title="Patron Dashboard")

# View Reports
@patron_bp.route('/view_reports')
@login_required
def view_reports():
    if current_user.role != 'patron':
        return redirect(url_for('unauthorized'))

    # Implementation for viewing financial reports can be added here
    return render_template('patron/view_reports.html', title="Financial Reports")

# Send Announcements
@patron_bp.route('/send_announcements', methods=['GET', 'POST'])
@login_required
def send_announcements():
    if current_user.role != 'patron':
        return redirect(url_for('unauthorized'))

    if request.method == 'POST':
        # Logic to send announcements (e.g., email or messaging) would go here
        flash('Announcement sent successfully!', 'success')
        return redirect(url_for('patron.send_announcements'))

    return render_template('patron/send_announcements.html', title="Send Announcements")
