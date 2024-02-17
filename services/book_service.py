import json
import os
import re
from urllib import parse
from collections import Counter

import nltk
import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from tabulate import tabulate
from tqdm import tqdm
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style


class BookService:
    service_books = None

    @staticmethod
    def download_neccessary_nltk_data() -> None:
        # Check if NLTK data is already downloaded and download if not
        if not nltk.data.find('tokenizers/punkt'):
            nltk.download('punkt')
        if not nltk.data.find('corpora/stopwords'):
            nltk.download('stopwords')

    @staticmethod
    def fetch_book_data() -> None:
        if BookService.service_books:
            return

        BookService.service_books = BookService.__load_books_from_json()  # Fetch book data online from Gutenberg
        if not BookService.service_books:
            BookService.service_books = BookService.__get_all_gutenberg_books()  # Fetch book data online from Gutenberg

        BookService.service_books = BookService.__expand_books_with_or(BookService.service_books)
        BookService.__save_books_to_json(BookService.service_books)

    @staticmethod
    def get_books() -> list:
        if BookService.service_books:
            return BookService.service_books

        BookService.fetch_book_data()
        return BookService.service_books

    @staticmethod
    def get_stats(book_title: str):
        # TODO: Implement
        #  Implement getting stats for a book
        pass

    @staticmethod
    def is_book_available(book_title: str) -> bool:
        # Check if any dictionary in service_books has the given book_title
        return any(book['name'] == book_title for book in BookService.service_books)

    @staticmethod
    def __load_books_from_json():
        if os.path.exists("book_data.json"):
            with open("book_data.json", "r") as file:
                books = json.load(file)
            return books
        else:
            return None

    @staticmethod
    def __save_books_to_json(books):
        with open("book_data.json", "w") as file:
            json.dump(books, file)

    @staticmethod
    def __get_books_from_page(url):
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            book_links = soup.find_all('li', class_='booklink')

            book_data = []
            for link in book_links:
                name = link.find('span', class_='title').text.strip()
                relative_url = link.find('a')['href']
                full_url = "https://www.gutenberg.org" + relative_url
                book_data.append({'name': name, 'url': full_url})

            return book_data
        else:
            print("Failed to fetch Gutenberg books:", response.status_code)
            return None

    @staticmethod
    def __get_all_gutenberg_books():
        base_url = "https://www.gutenberg.org/ebooks/search/?start_index={}"
        start_index = 1
        all_books = []

        os.system('cls' if os.name in ('nt', 'dos') else 'clear')
        with tqdm(total=1000, desc="Fetching books", position=1, leave=True) as pbar:
            while True:
                url = base_url.format(start_index)
                books_on_page = BookService.__get_books_from_page(url)

                if books_on_page:
                    all_books.extend(books_on_page)
                    start_index += 25
                    pbar.update(25)
                else:
                    os.system('cls' if os.name in ('nt', 'dos') else 'clear')
                    print("Failed to fetch books. Exiting loop.")
                    break

        return all_books

    @staticmethod
    def __expand_books_with_or(names_and_urls):
        expanded_books = []
        for book in names_and_urls:
            name = book['name']
            url = book['url']

            # Check if the name contains the pattern "{name1}; Or, {name2}"
            if '; Or, ' in name:
                name_parts = name.split('; Or, ')
                for part in name_parts:
                    expanded_books.append({'name': part.strip(), 'url': url})
            elif '; or, ' in name:
                name_parts = name.split('; or, ')
                for part in name_parts:
                    expanded_books.append({'name': part.strip(), 'url': url})
            else:
                expanded_books.append(book)
        return expanded_books

    @staticmethod
    def get_books_by_search(search_term: str):
        encoded_search_term = parse.quote(search_term)
        # Construct the URL with the encoded search term
        url = f"https://www.gutenberg.org/ebooks/search/?query={encoded_search_term}&submit_search=Go%21"
        books_on_page = BookService.__get_books_from_page(url)
        if books_on_page:
            books_on_page = BookService.__expand_books_with_or(books_on_page)

            # Add new books to our data
            made_changes = False
            for book in books_on_page:
                if not BookService.is_book_available(book['name']):
                    BookService.service_books.append(book)
                    made_changes = True
            if made_changes:
                BookService.__save_books_to_json(BookService.service_books)

            return books_on_page

        return None


BookService.download_neccessary_nltk_data()
BookService.fetch_book_data()