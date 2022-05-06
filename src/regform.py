from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email


class RegisterForm(FlaskForm):
  user_email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
  user_name = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
  user_password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
  user_confirm_password = PasswordField('Re-enter your password', validators=[InputRequired(), Length(min=8, max=80)])
