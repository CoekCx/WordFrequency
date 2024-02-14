import requests
from bs4 import BeautifulSoup
import nltk
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter


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

    print("Total words in Moby Dick:", total_words)
    print("Unique words in Moby Dick:", unique_words)
    print("\nTop 10 most common words:")
    for word, count in word_count:
        print(f"{word}: {count}")


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

    # Make words lowercase
    lowercase_words = make_words_lowercase(words)

    # Check if words were converted to lowercase successfully
    if lowercase_words:
        print("Words converted to lowercase successfully!")
    else:
        print("Failed to convert words to lowercase.")

    # Make words lowercase
    filtered_lowercase_words = remove_non_words(lowercase_words)

    # Check if words were converted to lowercase successfully
    if filtered_lowercase_words:
        print("Removed non words successfully!")
    else:
        print("Failed to removed non words.")

    # Load stop words
    stop_words = load_stop_words()

    # Check if stop words were loaded successfully
    if stop_words:
        print("Stop words loaded successfully!")
    else:
        print("Failed to load stop words.")

    # Call remove_stop_words() to filter out stop words
    filtered_words = remove_stop_words(filtered_lowercase_words, stop_words)

    # Check if stop words were removed successfully
    if filtered_words:
        print("Stop words removed successfully!")
    else:
        print("Failed to remove stop words.")

    # Call analyze_text() to analyze the processed text
    analyze_text(filtered_words)


if __name__ == '__main__':
    main()
