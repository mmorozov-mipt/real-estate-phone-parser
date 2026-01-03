"""
Real Estate Phone Parser
------------------------

Этот скрипт умеет заходить на сайт по ссылке и искать на странице номера телефонов.

Теперь у него 2 режима работы:

1) ОДИН САЙТ
   python3 parser.py https://example.com/page

   Скрипт обрабатывает одну страницу.

2) СПИСОК ССЫЛОК ИЗ ФАЙЛА
   python3 parser.py urls.txt

   В файле urls.txt каждая строка – это отдельная ссылка.
   Скрипт по очереди обходит все эти страницы и собирает телефоны со всех.

Результат в обоих режимах:
- телефоны сохраняются в файл phones.txt (по одному номеру на строку)
- на экран выводится статистика
"""

import sys
import re
from typing import List, Set

import requests
from bs4 import BeautifulSoup


# ---------------------------------------------
# Правило для поиска телефонов
# ---------------------------------------------
PHONE_REGEX = re.compile(
    r"""
    (\+?\d[\d\-\s\(\)]{7,}\d)
    """,
    re.VERBOSE,
)


# ---------------------------------------------
# Скачиваем страницу по ссылке
# ---------------------------------------------
def fetch_html(url: str) -> str:
    """
    Загружает HTML код сайта по ссылке.
    """

    # Притворяемся обычным браузером, сайты так реагируют спокойнее
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        )
    }

    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
    return response.text


# ---------------------------------------------
# Достаём читаемый текст из HTML
# ---------------------------------------------
def extract_text(html: str) -> str:
    """
    Удаляем HTML теги и оставляем только видимый текст.
    """

    soup = BeautifulSoup(html, "html.parser")

    # Удаляем то, что пользователь не видит
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator=" ")
    # Убираем лишние пробелы
    return " ".join(text.split())


# ---------------------------------------------
# Ищем телефоны в тексте
# ---------------------------------------------
def find_raw_phones(text: str) -> List[str]:
    """
    Ищем всё, что похоже на телефон, по регулярному выражению.
    """
    return PHONE_REGEX.findall(text)


# ---------------------------------------------
# Нормализуем телефон (делаем аккуратным)
# ---------------------------------------------
def normalize_phone(raw: str) -> str:
    """
    Приводим телефоны к единому виду.

    Пример:
    "+7 (999) 123-45-67" -> "+79991234567"
    "8 912 333 22 11"   -> "89123332211"
    """

    has_plus = raw.strip().startswith("+")
    # оставляем только цифры
    digits = re.sub(r"\D", "", raw)

    if not digits:
        return ""

    if has_plus:
        return "+" + digits

    return digits


def normalize_phones(raw_phones: List[str]) -> Set[str]:
    """
    Применяем нормализацию ко всем телефонам и убираем повторы.
    """
    result: Set[str] = set()
    for raw in raw_phones:
        norm = normalize_phone(raw)
        if norm:
            result.add(norm)
    return result


# ---------------------------------------------
# Сохраняем телефоны в файл
# ---------------------------------------------
def save_phones(phones: Set[str], path: str = "phones.txt") -> None:
    """
    Сохраняет номера в файл, по одному номеру в строке.
    """
    with open(path, "w", encoding="utf-8") as f:
        for p in sorted(phones):
            f.write(p + "\n")


# ---------------------------------------------
# Работа с режимом "список ссылок"
# ---------------------------------------------
def load_urls_from_file(path: str) -> List[str]:
    """
    Читает файл со списком ссылок.
    В файле:
      - каждая строка это URL
      - пустые строки и строки, начинающиеся с #, игнорируются
    """
    urls: List[str] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):
                continue
            urls.append(line)
    return urls


def process_single_url(url: str) -> Set[str]:
    """
    Обрабатывает один URL и возвращает множество телефонов, найденных на этой странице.
    """
    print(f"Открываю страницу: {url}")

    try:
        html = fetch_html(url)
    except Exception as e:
        print(f"Не смог открыть страницу. Ошибка: {e}")
        return set()

    text = extract_text(html)
    raw_matches = find_raw_phones(text)
    print(f"  Найдено совпадений (сырых): {len(raw_matches)}")
    unique = normalize_phones(raw_matches)
    print(f"  Уникальных телефонов после очистки: {len(unique)}")
    return unique


# ---------------------------------------------
# Главная функция
# ---------------------------------------------
def main() -> None:
    """
    Определяет режим работы и запускает скрипт.
    """

    if len(sys.argv) < 2:
        print("Как пользоваться:")
        print("  Один сайт: python3 parser.py https://example.com/page")
        print("  Список сайтов из файла: python3 parser.py urls.txt")
        sys.exit(1)

    arg = sys.argv[1]

    # Если аргумент начинается с http:// или https:// – считаем, что это один URL
    if arg.startswith("http://") or arg.startswith("https://"):
        print("Режим: один сайт")
        phones = process_single_url(arg)
    else:
        # Иначе считаем, что это путь к файлу со списком ссылок
        print("Режим: список ссылок из файла")
        print(f"Читаю ссылки из: {arg}")
        try:
            urls = load_urls_from_file(arg)
        except Exception as e:
            print(f"Не удалось прочитать файл с ссылками. Ошибка: {e}")
            sys.exit(1)

        print(f"Найдено ссылок: {len(urls)}")
        phones: Set[str] = set()
        for url in urls:
            new_phones = process_single_url(url)
            phones |= new_phones  # объединяем множества

    # Финальный результат
    if phones:
        save_phones(phones, "phones.txt")
        print()
        print(f"ИТОГО: уникальных телефонов со всех страниц: {len(phones)}")
        print("Телефоны сохранены в файл phones.txt")
    else:
        print("Телефонов не найдено.")


if __name__ == "__main__":
    main()
