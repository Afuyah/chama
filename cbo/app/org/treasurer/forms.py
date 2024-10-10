from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange

class ContributionForm(FlaskForm):
    member = SelectField('Member', coerce=int, validators=[DataRequired()])
    amount = IntegerField('Amount', validators=[DataRequired(), NumberRange(min=1)])

class FineForm(FlaskForm):
    member = SelectField('Member', coerce=int, validators=[DataRequired()])
    reason = StringField('Reason', validators=[DataRequired()])
    amount = IntegerField('Amount', validators=[DataRequired(), NumberRange(min=1)])
