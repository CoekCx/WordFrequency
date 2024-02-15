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


# <editor-fold desc="Project Setup">


# This should be run once before the first run of the script
def download_neccessary_nltk_data():
    nltk.download('punkt')
    nltk.download('stopwords')


# </editor-fold>

# <editor-fold desc="Book Data Acquisition">

def load_books_from_json():
    if os.path.exists("book_data.json"):
        with open("book_data.json", "r") as file:
            books = json.load(file)
        return books
    else:
        return None


def save_books_to_json(books):
    with open("book_data.json", "w") as file:
        json.dump(books, file)


def get_books_from_page(url):
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


def get_all_gutenberg_books():
    base_url = "https://www.gutenberg.org/ebooks/search/?start_index={}"
    start_index = 1
    all_books = []

    os.system('cls' if os.name in ('nt', 'dos') else 'clear')
    with tqdm(total=1000, desc="Fetching books", position=1, leave=True) as pbar:
        while True:
            url = base_url.format(start_index)
            books_on_page = get_books_from_page(url)

            if books_on_page:
                all_books.extend(books_on_page)
                start_index += 25
                pbar.update(25)
            else:
                os.system('cls' if os.name in ('nt', 'dos') else 'clear')
                print("Failed to fetch books. Exiting loop.")
                break

    return all_books


def get_books_by_search(search_term: str):
    encoded_search_term = parse.quote(search_term)
    # Construct the URL with the encoded search term
    url = f"https://www.gutenberg.org/ebooks/search/?query={encoded_search_term}&submit_search=Go%21"
    books_on_page = get_books_from_page(url)
    if books_on_page:
        return expand_books_with_or(books_on_page)

    return None


def expand_books_with_or(names_and_urls):
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


def search_for_book(search_term):
    books = get_books_by_search(search_term)
    if not books:
        return None

    book_names = [book['name'] for book in books]

    style = Style.from_dict({
        'input': '#44ff44',
        'placeholder': '#888888',
    })

    completer = WordCompleter(book_names, ignore_case=True, match_middle=True)

    # Prompt text with a green background
    prompt_text = [
        ('class:prompt', 'Enter title - Searched (Leave blank for return): '),
        ('class:input', ''),
    ]

    os.system('cls' if os.name in ('nt', 'dos') else 'clear')
    input_book = prompt(prompt_text, style=style, completer=completer)
    if input_book.strip() in book_names:
        global_books.extend(books)
        return input_book.strip()

    return None


def prompt_user_for_book(books: list):
    book_names = [book['name'] for book in books]

    style = Style.from_dict({
        'input': '#44ff44',
        'placeholder': '#888888',
    })

    completer = WordCompleter(book_names, ignore_case=True, match_middle=True)

    # Prompt text with a green background
    prompt_text = [
        ('class:prompt', 'Enter title (Search if not offered): '),
        ('class:input', ''),
    ]

    while True:
        os.system('cls' if os.name in ('nt', 'dos') else 'clear')
        input_book = prompt(prompt_text, style=style, completer=completer)
        if input_book.strip() in book_names:
            return input_book.strip()
        else:
            found_book = search_for_book(input_book.strip())
            if found_book:
                return found_book.strip()


# </editor-fold>

# <editor-fold desc="Book Processing">


def fetch_book(book_url: str):
    url = f'{book_url}.txt.utf-8'
    response = requests.get(url)

    if response.status_code == 200:
        return response.text
    else:
        print("Failed to fetch book:", response.status_code)
        return None


def extract_words(text):
    words = word_tokenize(text)
    return words


def make_words_lowercase(words):
    lowercase_words = [word.lower() for word in words]
    return lowercase_words


def remove_non_words(words):
    cleaned_words = [word for word in words if re.match(r'^[a-zA-Z]+$', word)]
    return cleaned_words


def load_stop_words():
    stop_words = set(stopwords.words('english'))
    return stop_words


def remove_stop_words(words, stop_words):
    filtered_words = [word for word in words if word not in stop_words]
    return filtered_words


def analyze_text(book_name, words):
    total_words = len(words)
    unique_words = len(set(words))
    word_count = Counter(words).most_common(10)  # Top 10 most common words

    # Prettify output with colors
    colored_word_count = [(f"\033[94m{word}\033[0m", f"\033[92m{count}\033[0m") for word, count in word_count]

    # Prepare data for tabular display
    table_data = [
                     [f"Total words:", f"\033[95m{total_words}\033[0m"],
                     [f"Unique words:", f"\033[95m{unique_words}\033[0m"],
                     ["", ""],  # Empty row for spacing
                     ["\033[96mTop 10 most common words:\033[0m", ""],
                 ] + colored_word_count

    # Print the table
    os.system('cls' if os.name in ('nt', 'dos') else 'clear')
    print(tabulate(table_data, headers=[f"\033[96m{book_name}\033[0m", "Count"], tablefmt="fancy_grid"))


# </editor-fold>

global_books = load_books_from_json()


def main():
    # Load book data
    if not global_books:
        books = get_all_gutenberg_books()  # Fetch book data online from Gutenberg
        if not books:
            os.system('cls' if os.name in ('nt', 'dos') else 'clear')
            print("Failed to get the list of Gutenberg books.")
            input()
            return

        books = expand_books_with_or(books)
        save_books_to_json(books)

    # Prompt user to select a book
    selected_book_name = prompt_user_for_book(global_books)
    selected_book_url = [x['url'] for x in global_books if x['name'] == selected_book_name][0]

    steps = [
        'Fetch HTML (text) content of the book',
        'Extract words from text content',
        'Make words lowercase',
        'Remove non-words',
        'Load stop words',
        'Remove stop words',
    ]

    # Process book
    os.system('cls' if os.name in ('nt', 'dos') else 'clear')
    with tqdm(total=len(steps), desc="Processing steps", position=0, leave=True) as pbar:
        def take_next_step(next_step: str):
            pbar.update(1)
            pbar.set_postfix(ID=next_step)

        for index, step in enumerate(steps):
            if step == 'Fetch HTML (text) content of the book':
                text_content = fetch_book(selected_book_url)
                if text_content:
                    take_next_step(steps[index + 1])
                else:
                    os.system('cls' if os.name in ('nt', 'dos') else 'clear')
                    print("Failed to fetch HTML content of Moby Dick.")
                    return

            elif step == 'Extract words from text content':
                words = extract_words(text_content)
                if words:
                    take_next_step(steps[index + 1])
                else:
                    os.system('cls' if os.name in ('nt', 'dos') else 'clear')
                    print("Failed to extract words from text content.")
                    return

            elif step == 'Make words lowercase':
                lowercase_words = make_words_lowercase(words)
                if lowercase_words:
                    os.system('cls' if os.name in ('nt', 'dos') else 'clear')
                    take_next_step(steps[index + 1])
                else:
                    os.system('cls' if os.name in ('nt', 'dos') else 'clear')
                    print("Failed to convert words to lowercase.")
                    return

            elif step == 'Remove non-words':
                filtered_lowercase_words = remove_non_words(lowercase_words)
                if filtered_lowercase_words:
                    take_next_step(steps[index + 1])
                else:
                    os.system('cls' if os.name in ('nt', 'dos') else 'clear')
                    print("Failed to remove non-words.")
                    return

            elif step == 'Load stop words':
                stop_words = load_stop_words()
                if stop_words:
                    take_next_step(steps[index + 1])
                else:
                    os.system('cls' if os.name in ('nt', 'dos') else 'clear')
                    print("Failed to load stop words.")
                    return

            elif step == 'Remove stop words':
                filtered_words = remove_stop_words(filtered_lowercase_words, stop_words)
                if not filtered_words:
                    os.system('cls' if os.name in ('nt', 'dos') else 'clear')
                    print("Failed to remove stop words.")
                    return

    # Analyze the processed text
    analyze_text(selected_book_name, filtered_words)


if __name__ == '__main__':
    main()
