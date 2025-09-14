import requests
from bs4 import BeautifulSoup


def requests_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    return None


def bs_parser(content):
    return BeautifulSoup(content.decode('utf-8'), 'html.parser')


def get_book_info(isbn):
    api_url = 'https://openlibrary.org/search.json?isbn=' + isbn
    response = requests.get(api_url, timeout=5)
    if response.status_code == 200:
        response_json = response.json()
        if response_json['numFound'] > 0:
            book_info = response_json['docs'][0]
            book_info['isbn'] = isbn
            return book_info
    return None


def get_serie_name(url, already_past=False):
    content = requests_content(url)
    if content is not None:
        url_parsed = bs_parser(content)
        if not already_past:
            end_url = url_parsed.find(attrs={'class': 'card-link'}).get('href')
            url = 'https://www.bdbase.fr' + end_url
            return get_serie_name(url, already_past=True)
        serie_name = url_parsed.find(attrs={'class': 'book-data-summary'}).find('div').text
        return serie_name
    return None
