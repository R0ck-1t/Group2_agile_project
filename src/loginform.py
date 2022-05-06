from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length



class LoginForm(FlaskForm):
  user_name = StringField('Username', validators=[InputRequired(), Length(min=3, max=24)])
  user_password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
  remember = BooleanField('Remember me.')