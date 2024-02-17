from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class BookLookupForm(FlaskForm):
    title = StringField('Book Title', validators=[DataRequired()])
    submit = SubmitField('Submit')
