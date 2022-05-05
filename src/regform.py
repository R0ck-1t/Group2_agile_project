from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email


class RegisterForm(FlaskForm):
  email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
  useremail = StringField('Email', validators=[InputRequired(), Length(min=25, max=40)])
  username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
  password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
  confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), Length(min=8, max=80)] )