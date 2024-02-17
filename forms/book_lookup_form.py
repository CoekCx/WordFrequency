from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class BookLookupForm(FlaskForm):
    title = StringField('Book Title')
    submit = SubmitField('Submit')
