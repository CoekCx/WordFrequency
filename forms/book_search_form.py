from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired


class BookSearchForm(FlaskForm):
    def __init__(self, book_options, **kwargs):
        super().__init__(**kwargs)
        self.title.choices = book_options

    title = SelectField('Book Title', validators=[DataRequired()])
    submit = SubmitField('Submit')
    back = SubmitField('Back')
