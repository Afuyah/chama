from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from .forms import AddMemberForm
from app.models import Member
from app import db
from werkzeug.security import generate_password_hash

# Define Blueprint
chairman_bp = Blueprint('chairman', __name__)

# Chairman Dashboard
@chairman_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role.name.lower() != 'chairman':
        return redirect(url_for('main.unauthorized'))  # Ensure to access role name here
    return render_template('chairman/dashboard.html', title="Chairman's Dashboard")

# Route to add a new member
@chairman_bp.route('/add_member', methods=['GET', 'POST'])
@login_required
def add_member():
    if current_user.role.name.lower() != 'chairman':
        return redirect(url_for('main.unauthorized'))  # Ensure to access role name here

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
        
        new_member.set_password(form.national_id.data)  # Use the method to set the password

        try:
            db.session.add(new_member)
            db.session.commit()
            flash('New member added successfully!', 'success')
            return redirect(url_for('chairman.dashboard'))
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            flash(f'Error adding new member: {str(e)}', 'danger')  # Provide error context

    elif form.errors:
        for error in form.errors.values():
            flash(error[0], 'danger')  # Flash form validation errors

    return render_template('chairman/add_member.html', form=form, title="Add Member")


@chairman_bp.route('/view_members', methods=['GET'])
def view_members():
    members = Member.query.all()  # Fetch all members from the database
    return render_template('chairman/view_members.html', members=members)



@chairman_bp.route('/manage_events', methods=['GET', 'POST'])
def manage_events():
    if request.method == 'POST':
        # Logic to handle event creation or updates
        pass
    # Fetch events from the database if necessary
    # events = Event.query.all()  # Uncomment and define Event model accordingly
    return render_template('chairman/manage_events.html')  # Create this template

@chairman_bp.route('/edit_member/<int:member_id>', methods=['GET', 'POST'])
@login_required
def edit_member(member_id):
    if current_user.role.name.lower() != 'chairman':
        return redirect(url_for('main.unauthorized'))

    member = Member.query.get_or_404(member_id)
    form = AddMemberForm(obj=member)  # Prefill form with current member data

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
