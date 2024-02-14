import requests
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter


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


# TODO: Task 5: Make the words lowercase

# TODO: Task 6: Load in stop words

# TODO: Task 7: Remove stop words in Moby Dick

# TODO: Task 8: We have the answer

# TODO: Task 9: The most common word

def main():
    # Fetch Moby Dick content
    html_content = fetch_moby_dick()

    # Check if content was fetched successfully
    if html_content:
        print("HTML content of Moby Dick fetched successfully!")
    else:
        print("Failed to fetch HTML content of Moby Dick.")

    # Extract text from HTML content
    text_content = extract_text_from_html(html_content)

    # Check if text was extracted successfully
    if text_content:
        print("Text extracted successfully!")
    else:
        print("Failed to extract text from HTML content.")

    # Extract words from text content
    words = extract_words(text_content)

    # Check if words were extracted successfully
    if words:
        print("Words extracted successfully!")
    else:
        print("Failed to extract words from text content.")


if __name__ == '__main__':
    main()
