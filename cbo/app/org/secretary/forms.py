from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class AttendanceForm(FlaskForm):
    members = SelectMultipleField('Members', coerce=int)  # A list of member IDs
    status = SelectField('Attendance Status', choices=[('Present', 'Present'), ('Absent', 'Absent'), ('Late', 'Late')], validators=[DataRequired()])
    submit = SubmitField('Record Attendance')


class EventForm(FlaskForm):
    name = StringField('Event Name', validators=[DataRequired()])
    description = TextAreaField('Event Description', validators=[DataRequired()])
