from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, TextAreaField
from wtforms.validators import DataRequired

class AttendanceForm(FlaskForm):
    members = SelectMultipleField('Members', coerce=int, validators=[DataRequired()])
    status = SelectField('Status', choices=[('present', 'Present'), ('absent', 'Absent'), ('late', 'Late')], validators=[DataRequired()])

class EventForm(FlaskForm):
    name = StringField('Event Name', validators=[DataRequired()])
    description = TextAreaField('Event Description', validators=[DataRequired()])
