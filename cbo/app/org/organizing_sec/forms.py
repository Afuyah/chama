from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField
from wtforms.validators import DataRequired

class AttendanceForm(FlaskForm):
    member = SelectField('Member', coerce=int, validators=[DataRequired()])
    status = SelectField('Status', choices=[('Present', 'Present'), ('Late', 'Late'), ('Absent', 'Absent')], validators=[DataRequired()])
    fine_amount = IntegerField('Fine Amount', default=0)
