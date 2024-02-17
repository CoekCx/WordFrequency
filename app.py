from flask import Flask, render_template
from flask_bootstrap import Bootstrap

from forms.book_search_form import BookSearchForm
from services.book_service import BookService

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f3d7a5b0828bb0b12c3ecdd2999d3c7f'

# Initialize Flask-Bootstrap
bootstrap = Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = BookSearchForm()
    if form.validate_on_submit():
        # Process form data here
        title = form.title.data
        # Do something with the data (e.g., store it in a database)
        return f'Book title: {title}'

    books = BookService.get_books()
    book_titles = list(set([book['name'] for book in books]))
    return render_template('index.html', form=form, book_titles=book_titles)


if __name__ == '__main__':
    BookService.download_neccessary_nltk_data()
    app.run(port=5000, debug=True)
