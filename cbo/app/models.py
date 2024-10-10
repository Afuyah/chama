from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, FloatField, DateTimeField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, EqualTo

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(max=15)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=128)])
    residence = StringField('Residence', validators=[DataRequired(), Length(max=100)])
    county = StringField('County', validators=[DataRequired(), Length(max=100)])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female')], validators=[DataRequired()])
    age = FloatField('Age', validators=[DataRequired(), NumberRange(min=1)])
    role = SelectField('Role', choices=[('Chairman', 'Chairman'), 
                                         ('Secretary', 'Secretary'), 
                                         ('Organizing Secretary', 'Organizing Secretary'), 
                                         ('Treasurer', 'Treasurer'), 
                                         ('Member Representative', 'Member Representative'),
                                         ('Member', 'Member')], validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ContributionForm(FlaskForm):
    amount = FloatField('Contribution Amount', validators=[DataRequired(), NumberRange(min=1)])
    date = DateTimeField('Date', default=datetime.utcnow, format='%Y-%m-%d', validators=[Optional()])
    submit = SubmitField('Submit Contribution')

class FineForm(FlaskForm):
    amount = FloatField('Fine Amount', validators=[DataRequired(), NumberRange(min=1)])
    reason = StringField('Reason', validators=[Optional(), Length(max=200)])
    date = DateTimeField('Date', default=datetime.utcnow, format='%Y-%m-%d', validators=[Optional()])
    submit = SubmitField('Submit Fine')

class AttendanceForm(FlaskForm):
    status = SelectField('Attendance Status', choices=[('Present', 'Present'), ('Absent', 'Absent'), ('Late', 'Late')], validators=[DataRequired()])
    date = DateTimeField('Date', default=datetime.utcnow, format='%Y-%m-%d', validators=[Optional()])
    submit = SubmitField('Submit Attendance')
