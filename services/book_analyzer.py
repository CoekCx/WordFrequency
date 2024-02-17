import re
from collections import Counter

import requests
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


class BookAnalyzer:
    @staticmethod
    def analyze_book(book_url) -> str or dict:
        text_content = BookAnalyzer.__fetch_book(book_url)
        if not text_content:
            return "Failed to fetch HTML content of Moby Dick."

        words = BookAnalyzer.__extract_words(text_content)
        if not words:
            return "Failed to extract words from text content."

        lowercase_words = BookAnalyzer.__make_words_lowercase(words)
        if not lowercase_words:
            return "Failed to convert words to lowercase."

        filtered_lowercase_words = BookAnalyzer.__remove_non_words(lowercase_words)
        if not filtered_lowercase_words:
            return "Failed to remove non-words."

        stop_words = BookAnalyzer.__load_stop_words()
        if not stop_words:
            return "Failed to load stop words."

        filtered_words = BookAnalyzer.__remove_stop_words(filtered_lowercase_words, stop_words)
        if not filtered_words:
            return "Failed to remove stop words."

        # Analyze the processed text
        return BookAnalyzer.__analyze_text(filtered_words)

    @staticmethod
    def __fetch_book(book_url: str):
        url = f'{book_url}.txt.utf-8'
        response = requests.get(url)

        if response.status_code == 200:
            return response.text
        else:
            print("Failed to fetch book:", response.status_code)
            return None

    @staticmethod
    def __extract_words(text):
        words = word_tokenize(text)
        return words

    @staticmethod
    def __make_words_lowercase(words):
        lowercase_words = [word.lower() for word in words]
        return lowercase_words

    @staticmethod
    def __remove_non_words(words):
        cleaned_words = [word for word in words if re.match(r'^[a-zA-Z]+$', word)]
        return cleaned_words

    @staticmethod
    def __load_stop_words():
        stop_words = set(stopwords.words('english'))
        return stop_words

    @staticmethod
    def __remove_stop_words(words, stop_words):
        filtered_words = [word for word in words if word not in stop_words]
        return filtered_words

    @staticmethod
    def __analyze_text(words):
        total_words = len(words)
        unique_words = len(set(words))
        word_count = Counter(words).most_common(10)  # Top 10 most common words
        analasys_data = {
            'total_words': total_words,
            'unique_words': unique_words,
            'word_count': word_count,
        }
        return analasys_data
