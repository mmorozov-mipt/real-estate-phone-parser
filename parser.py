import re
import requests
from bs4 import BeautifulSoup

PHONE_REGEX = r'(\+?\d[\d\-\s\(\)]{7,}\d)'

def parse_phones(url: str) -> list:
    """
    Parse phone numbers from a one-page website
    """
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text(separator=' ')

    phones = re.findall(PHONE_REGEX, text)
    return list(set(phones))


if __name__ == "__main__":
    test_url = input("Enter website URL: ")
    phones = parse_phones(test_url)

    if phones:
        print("Found phone numbers:")
        for phone in phones:
            print(phone)
    else:
        print("No phone numbers found.")
