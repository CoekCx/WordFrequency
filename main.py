import os
import re
from collections import Counter

import nltk
import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from tabulate import tabulate
from tqdm import tqdm


# This should be run once before the first run of the script
def download_neccessary_nltk_data():
    nltk.download('punkt')
    nltk.download('stopwords')


def fetch_moby_dick():
    url = "https://www.gutenberg.org/files/2701/2701-h/2701-h.htm"  # URL of Moby Dick on Project Gutenberg
    response = requests.get(url)

    if response.status_code == 200:
        return response.text
    else:
        print("Failed to fetch Moby Dick:", response.status_code)
        return None


def extract_text_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text()
    return text.strip()


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


def analyze_text(words):
    total_words = len(words)
    unique_words = len(set(words))
    word_count = Counter(words).most_common(10)  # Top 10 most common words

    # Prettify output with colors
    colored_word_count = [(f"\033[94m{word}\033[0m", f"\033[92m{count}\033[0m") for word, count in word_count]

    # Prepare data for tabular display
    table_data = [
                     ["Total words in Moby Dick:", f"\033[95m{total_words}\033[0m"],
                     ["Unique words in Moby Dick:", f"\033[95m{unique_words}\033[0m"],
                     ["", ""],  # Empty row for spacing
                     ["\033[96mTop 10 most common words:\033[0m", ""],
                 ] + colored_word_count

    # Print the table
    os.system('cls' if os.name in ('nt', 'dos') else 'clear')
    print(tabulate(table_data, headers=["Word", "Count"], tablefmt="fancy_grid"))


def main():
    steps = [
        'Fetch HTML content of Moby Dick',
        'Extract text from HTML content',
        'Extract words from text content',
        'Make words lowercase',
        'Remove non-words',
        'Load stop words',
        'Remove stop words',
    ]

    os.system('cls' if os.name in ('nt', 'dos') else 'clear')
    with tqdm(total=len(steps), desc="Processing steps", position=0, leave=True) as pbar:
        def take_next_step(next_step: str):
            pbar.update(1)
            pbar.set_postfix(ID=next_step)

        for index, step in enumerate(steps):
            if step == 'Fetch HTML content of Moby Dick':
                html_content = fetch_moby_dick()
                if html_content:
                    take_next_step(steps[index + 1])
                else:
                    os.system('cls' if os.name in ('nt', 'dos') else 'clear')
                    print("Failed to fetch HTML content of Moby Dick.")
                    return

            elif step == 'Extract text from HTML content':
                text_content = extract_text_from_html(html_content)
                if text_content:
                    take_next_step(steps[index + 1])
                else:
                    os.system('cls' if os.name in ('nt', 'dos') else 'clear')
                    print("Failed to extract text from HTML content.")
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

    # Call analyze_text() to analyze the processed text
    analyze_text(filtered_words)


if __name__ == '__main__':
    main()
