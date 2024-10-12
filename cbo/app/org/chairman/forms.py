
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, IntegerField, SelectField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class AddMemberForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(max=15)])
    residence = StringField('Residence', validators=[DataRequired(), Length(max=100)])
    county = StringField('County', validators=[DataRequired(), Length(max=100)])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female')], validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    national_id = PasswordField('National ID', validators=[DataRequired(), Length(min=8, max=20)])
    submit = SubmitField('Add Member')

class ScheduleMeetingForm(FlaskForm):
    date = DateField('Meeting Date', format='%Y-%m-%d', validators=[DataRequired()])
    minutes = TextAreaField('Minutes', validators=[DataRequired()])
    submit = SubmitField('Schedule Meeting')

class ManageEventForm(FlaskForm):
    name = StringField('Event Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Event Description', validators=[DataRequired()])
    date = DateField('Event Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Create Event')

class ReportForm(FlaskForm):
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    report_type = SelectField('Report Type', choices=[
        ('contribution', 'Contribution Report'),
        ('attendance', 'Attendance Report'),
        ('fine', 'Fine Report'),
        ('event', 'Event Report')
    ], validators=[DataRequired()])
    submit = SubmitField('Generate Report')
