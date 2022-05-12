from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email

class submissionForm(FlaskForm):
    replit_name = StringField('Replit Name', validators=[InputRequired(), Length(min=0, max=32)])
    replit_link = StringField('Replit Link/URL', validators=[InputRequired(), Length(min=0, max=256)])
    replit_description = StringField('Short Description of Application', validators=[InputRequired(), Length(min=0, max=512)])