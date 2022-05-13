from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Length

class submissionForm(FlaskForm):
    replit_name = StringField('Replit Name', validators=[InputRequired(), Length(min=0, max=32)])
    replit_link = StringField('Replit Link', validators=[InputRequired(), Length(min=0, max=256)])
    replit_description = StringField('Short Description', validators=[InputRequired(), Length(min=0, max=512)])