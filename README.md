# Real Estate Phone Parser

Python tool for parsing phone numbers from one-page real estate websites.

## Project Goal
This project was developed as part of a personal application for selecting and analyzing real estate offers.
It automatically extracts contact phone numbers from simple landing pages and one-page websites.

## Technologies
- Python 3
- requests
- BeautifulSoup
- Regular Expressions

## How it works
1. Downloads HTML content of a webpage
2. Extracts visible text
3. Finds phone numbers using regex patterns
4. Removes duplicates

## Usage
```bash
pip install -r requirements.txt
python parser.py
