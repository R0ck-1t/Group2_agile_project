from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email

class UserForm(FlaskForm):
  bio = StringField('Bio', validators=[InputRequired(), Length(min=0, max=512)])