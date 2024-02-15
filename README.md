# Project Gutenberg Scraper and Text Analysis

This project is designed to scrape a novel from Project Gutenberg, extract words from the text using BeautifulSoup, and
analyze the word distribution using the Natural Language Toolkit (NLTK).

## Project Description

In this project, we use Python libraries such as prompt_toolkit, requests, BeautifulSoup, and NLTK to perform the
following tasks:

1. **Select Book**: Prompt user to select a book from either the 1000 most popular books on Gutenberg or from a search.
2. **Request Book**: Fetch the text content of the book from Project Gutenberg.
3. **Extract the words**: Tokenize the text into words using NLTK's word_tokenize() function.
4. **Make the words lowercase**: Convert all words to lowercase.
5. **Remove non-words**: Remove all non-words values.
6. **Load in stop words**: Load the list of stop words from NLTK.
7. **Remove stop words in Moby Dick**: Filter out the stop words from the list of words extracted from Moby Dick.
8. **Total and unique words**: Calculate the number of total and unique words.
9. **The most common words**: Calculate the frequency distribution of words and find the 10 most common word.

## Dependencies

- Python 3.9
- requests
- BeautifulSoup4
- nltk
- tabulate
- prompt_toolkit

## Installation

You can install the required dependencies using pip:

