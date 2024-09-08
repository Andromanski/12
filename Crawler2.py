import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import time

def get_html(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Проверка на ошибки HTTP
        return response.text
    except requests.RequestException as e:
        print(f"Ошибка при запросе {url}: {e}")
        return ""

def extract_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a', href=True)
    hrefs = [link['href'] for link in links if link['href'].startswith('http')]
    return hrefs

def is_php_site_with_params(url):
    try:
        parsed_url = urlparse(url)
        if 'index.php' in parsed_url.path and parse_qs(parsed_url.query):
            return True
        return False
    except Exception as e:
        print(f"Ошибка при анализе URL {url}: {e}")
        return False

start_url = 'https://example.com'  # Начальный URL
visited = set()
to_visit = [start_url]
all_links = []

while len(all_links) < 200 and to_visit:
    url = to_visit.pop(0)
    if url not in visited:
        visited.add(url)
        html = get_html(url)
        if html:
            links = extract_links(html)
            for link in links:
                if link not in all_links and len(all_links) < 200:
                    if is_php_site_with_params(link):
                        print(f"Найден PHP-сайт с параметрами: {link}")
                        all_links.append(link)
                        to_visit.append(link)
    time.sleep(1)  # Задержка между запросами

with open('sites.txt', 'w') as file:
    for link in all_links:
        file.write(link + '\n')

print("Ссылки на PHP-сайты с параметрами сохранены в файл sites.txt")
