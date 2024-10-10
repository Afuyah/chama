from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Member, Attendance, Contribution
from app import db
from .forms import ChangePasswordForm, ProfileForm

# Define Blueprint
member_bp = Blueprint('member', __name__)

# Member Dashboard
@member_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('member/dashboard.html', title="Member Dashboard")

# Manage Profile
@member_bp.route('/manage_profile', methods=['GET', 'POST'])
@login_required
def manage_profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.phone = form.phone.data
        # Additional fields can be updated as necessary
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('member.manage_profile'))
    return render_template('member/manage_profile.html', form=form, title="Manage Profile")

# Change Password
@member_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.old_password.data):
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('Password changed successfully!', 'success')
            return redirect(url_for('member.dashboard'))
        else:
            flash('Old password is incorrect.', 'danger')
    return render_template('member/change_password.html', form=form, title="Change Password")

# View Attendance
@member_bp.route('/view_attendance')
@login_required
def view_attendance():
    attendance_records = Attendance.query.filter_by(member_id=current_user.id).all()
    return render_template('member/view_attendance.html', attendance_records=attendance_records, title="View Attendance")

# View Financial Records
@member_bp.route('/view_financials')
@login_required
def view_financials():
    contributions = Contribution.query.filter_by(member_id=current_user.id).all()
    return render_template('member/view_financials.html', contributions=contributions, title="View Financial Records")
