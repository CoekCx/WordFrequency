from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class BookSearchForm(FlaskForm):
    title = StringField('Book Title')
    submit = SubmitField('Submit')
