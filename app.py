from flask import Flask, render_template, flash, jsonify
from flask_bootstrap import Bootstrap
from flask_toastr import Toastr
from flask_cors import CORS

from forms.book_lookup_form import BookLookupForm
from forms.book_search_form import BookSearchForm
from services.book_analyzer import BookAnalyzer
from services.book_service import BookService

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f3d7a5b0828bb0b12c3ecdd2999d3c7f'

CORS(app, supports_credentials=True)
bootstrap = Bootstrap(app)
toastr = Toastr(app)
toastr.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = BookLookupForm()
    if form.is_submitted():
        # Process form data here
        title = form.title.data
        if title == '':
            book_titles = BookService.get_book_titles()
            return render_template('index.html', form=form, book_titles=book_titles)

        if BookService.is_book_available(title):
            url, author = BookService.get_book_url_and_author(title)
            if url != 'URL not found':
                book_data = BookAnalyzer.analyze_book(title, author, url)
                return render_template('show-book-stats.html', data=book_data)

            flash("Couldn't find the URL for the book in our data!", 'error')
            book_titles = BookService.get_book_titles()
            return render_template('index.html', form=form, book_titles=book_titles)

        searched_books = BookService.get_books_by_search(title)
        if searched_books:
            searched_books_titles = list(set([book['name'] for book in searched_books]))
            book_options = [("", "Select a book")] + [(book_title, book_title) for book_title in
                                                      searched_books_titles]
            search_form = BookSearchForm(book_options)
            return render_template('search-books.html', form=search_form, searched_title=title)
        flash('No book found with that title!', 'info')

    book_titles = BookService.get_book_titles()
    return render_template('index.html', form=form, book_titles=book_titles)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
