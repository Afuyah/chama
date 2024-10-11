from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import Member  # Import the Member model instead of User
from app import db
from .forms import LoginForm  # Ensure your LoginForm is imported

# Define Blueprint
main_bp = Blueprint('main', __name__)

# Index route
@main_bp.route('/')
def index():
    return render_template('index.html')

# Login route
@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # Redirect if already logged in
        return redirect(url_for('member.dashboard'))  # Or any other page

    form = LoginForm()
    if form.validate_on_submit():
        # Query the Member model instead of User
        member = Member.query.filter_by(phone_number=form.username.data).first()  # Assuming phone number is the username
        if member and member.check_password(form.password.data):  # Ensure your Member model has check_password method
            login_user(member)  # Log in the member
            flash('Login successful!', 'success')
            return redirect(url_for('member.dashboard'))  # Redirect to the member dashboard or any other page
        else:
            flash('Login failed. Check your phone number and password.', 'danger')

    return render_template('main/login.html', form=form, title='Login')

@main_bp.route('/unauthorized')
def unauthorized():
    return render_template('main/unauthorized.html'), 403  # Or any status code you prefer


# Logout route
@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))  # Redirect to the home or login page
