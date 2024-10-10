from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from .forms import AddMemberForm
from app.models import Member
from app import db

# Define Blueprint
chairman_bp = Blueprint('chairman', __name__)

# Chairman Dashboard
@chairman_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'chairman':
        return redirect(url_for('unauthorized'))
    return render_template('chairman/dashboard.html', title="Chairman's Dashboard")

# Route to add a new member
@chairman_bp.route('/add_member', methods=['GET', 'POST'])
@login_required
def add_member():
    if current_user.role != 'chairman':
        return redirect(url_for('unauthorized'))
    
    form = AddMemberForm()
    if form.validate_on_submit():
        # Create a new member from form data
        new_member = Member(
            name=form.name.data,
            phone=form.phone.data,
            national_id=form.national_id.data,
            residence=form.residence.data,
            county=form.county.data,
            gender=form.gender.data,
            age=form.age.data
        )
        db.session.add(new_member)
        db.session.commit()
        flash('New member added successfully!', 'success')
        return redirect(url_for('chairman.add_member'))
    
    return render_template('chairman/add_member.html', form=form, title="Add Member")
