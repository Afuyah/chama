from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from .forms import ContributionForm, FineForm
from app.models import Member, Contribution, Fine
from app import db
from datetime import datetime

# Define Blueprint
treasurer_bp = Blueprint('treasurer', __name__)

# Treasurer Dashboard
@treasurer_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'treasurer':
        return redirect(url_for('unauthorized'))
    contributions = Contribution.query.all()
    fines = Fine.query.all()
    return render_template('treasurer/dashboard.html', title="Treasurer's Dashboard", contributions=contributions, fines=fines)

# Record member contributions
@treasurer_bp.route('/contribution', methods=['GET', 'POST'])
@login_required
def contribution():
    if current_user.role != 'treasurer':
        return redirect(url_for('unauthorized'))

    form = ContributionForm()
    if form.validate_on_submit():
        contribution = Contribution(
            member_id=form.member.data,
            amount=form.amount.data,
            date=datetime.now()
        )
        db.session.add(contribution)
        db.session.commit()
        flash('Contribution recorded successfully!', 'success')
        return redirect(url_for('treasurer.contribution'))
    
    members = Member.query.all()
    return render_template('treasurer/contribution.html', form=form, members=members, title="Record Contribution")

# Record member fines
@treasurer_bp.route('/fine', methods=['GET', 'POST'])
@login_required
def fine():
    if current_user.role != 'treasurer':
        return redirect(url_for('unauthorized'))

    form = FineForm()
    if form.validate_on_submit():
        fine = Fine(
            member_id=form.member.data,
            reason=form.reason.data,
            amount=form.amount.data,
            date=datetime.now()
        )
        db.session.add(fine)
        db.session.commit()
        flash('Fine recorded successfully!', 'success')
        return redirect(url_for('treasurer.fine'))

    members = Member.query.all()
    return render_template('treasurer/fine.html', form=form, members=members, title="Record Fine")
