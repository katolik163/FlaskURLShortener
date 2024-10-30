from datetime import datetime, timezone
from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeLocalField, IntegerField, PasswordField, SubmitField
from wtforms.validators import DataRequired, URL, Optional

class URLForm(FlaskForm):
    original_url = StringField('URL', validators=[DataRequired(), URL()])
    custom_short_url = StringField('Custom Short URL', validators=[Optional()])
    deletion_date = DateTimeLocalField('Deletion Date', validators=[Optional()], format='%Y-%m-%dT%H:%M', render_kw={'min': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M')})
    max_visits = IntegerField('Max Visits', validators=[Optional()])
    password = PasswordField('Password', validators=[Optional()])
    submit = SubmitField('Short')

class PasswordForm(FlaskForm):
    password = PasswordField('Enter Password', validators=[DataRequired()])
    submit = SubmitField('Submit')