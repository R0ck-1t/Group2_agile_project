from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email

class submissionForm(FlaskForm):
    dbName = StringField('Replit Name', validators=[InputRequired(), Length(min=0, max=32)])
    dbLink = StringField('Replit Link', validators=[InputRequired(), Length(min=0, max=256)])
    dbDescription = StringField('Short Description', validators=[InputRequired(), Length(min=0, max=512)])