from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from .forms import ContributionForm
from app.models import Contribution, Member
from app import db
from datetime import datetime

# Define Blueprint
member_rep_bp = Blueprint('member_rep', __name__)

# Member Representative Dashboard
@member_rep_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'member_rep':
        return redirect(url_for('main.unauthorized'))

    contributions = Contribution.query.order_by(Contribution.date.desc()).limit(10).all()
    return render_template('member_rep/dashboard.html', contributions=contributions, title="Member Representative Dashboard")

# Manage Contributions
@member_rep_bp.route('/manage_contributions', methods=['GET', 'POST'])
@login_required
def manage_contributions():
    if current_user.role != 'member_rep':
        return redirect(url_for('unauthorized'))

    form = ContributionForm()
    if form.validate_on_submit():
        contribution = Contribution(
            member_id=form.member.data,
            amount=form.amount.data,
            type=form.type.data,
            date=datetime.now()
        )
        db.session.add(contribution)
        db.session.commit()
        flash('Contribution added successfully!', 'success')
        return redirect(url_for('member_rep.manage_contributions'))

    members = Member.query.all()
    contributions = Contribution.query.all()
    return render_template('member_rep/manage_contributions.html', form=form, members=members, contributions=contributions, title="Manage Contributions")

# View Members
@member_rep_bp.route('/view_members')
@login_required
def view_members():
    if current_user.role != 'member_rep':
        return redirect(url_for('unauthorized'))

    members = Member.query.all()
    return render_template('member_rep/view_members.html', members=members, title="View Members")
