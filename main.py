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


# TODO: Task 3: Get the text from the HTML

# TODO: Task 4: Extract the words

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


if __name__ == '__main__':
    main()
