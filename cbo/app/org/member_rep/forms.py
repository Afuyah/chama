from flask_wtf import FlaskForm
from wtforms import SelectField, DecimalField, SelectField
from wtforms.validators import DataRequired

class ContributionForm(FlaskForm):
    member = SelectField('Member', coerce=int, validators=[DataRequired()])
    amount = DecimalField('Amount', validators=[DataRequired()])
    type = SelectField('Contribution Type', choices=[('Monthly Contribution', 'Monthly Contribution'), ('Fine Payment', 'Fine Payment')], validators=[DataRequired()])
