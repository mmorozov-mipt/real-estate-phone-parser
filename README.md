# Real Estate Phone Parser

Simple Python tool for extracting phone numbers from real estate landing pages and one-page websites.

The project was created for educational purposes and as part of a personal application for selecting and analyzing property offers.

## Project goal

The script:
- downloads HTML content of a given page
- extracts visible text
- finds phone numbers using regular expressions
- normalizes and deduplicates results
- saves unique phone numbers to a text file

## Technologies

- Python 3
- requests
- BeautifulSoup4
- regular expressions (regex)

## Installation

1. Install Python 3.
2. Install required libraries:

    pip install -r requirements.txt

## How to run

Run parser with site URL as argument:

    python3 parser.py https://example.com/page

On Windows it can look like this:

    python parser.py https://example.com/page

If you do not pass a URL, the script will print a short usage message and exit.

## Output

The script creates a file:

    phones.txt

One phone number per line, already normalized and deduplicated.

In the console it prints for example:

    Открываю страницу: https://example.com/page
    Найдено совпадений (сырых): 12
    Уникальных телефонов после очистки: 5
    Телефоны сохранены в файл phones.txt

## Example use case

Used to collect contact phone numbers from real estate landing pages in order to build a simple dataset
for further analysis and filtering of property offers.

This project also demonstrates:

- basic HTTP requests handling
- parsing HTML with BeautifulSoup
- using regular expressions for phone extraction
- simple data cleaning and export

## Disclaimer

This project is intended for educational and personal use only.
Please respect website Terms of Service and local legislation when scraping.
Do not use the script for spam or unlawful data collection.
