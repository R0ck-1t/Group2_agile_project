from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Length

class commentForm(FlaskForm):
    content = StringField('comment content:', validators=[InputRequired(), Length(min=0, max=512)])
    