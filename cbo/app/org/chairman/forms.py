from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length

class AddMemberForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    phone = StringField('Phone', validators=[DataRequired(), Length(max=15)])
    national_id = StringField('National ID', validators=[DataRequired(), Length(max=20)])
    residence = StringField('Residence', validators=[DataRequired(), Length(max=100)])
    county = StringField('County', validators=[DataRequired(), Length(max=50)])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female')], validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
