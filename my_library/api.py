import requests
from bs4 import BeautifulSoup


def handle_requests(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response
    except requests.exceptions.Timeout:
        print('Timeout lors de la requête')
    except requests.exceptions.RequestException as e:
        print(f'Erreur lors de la requête : {e}')
    return None


def bs_parser(content):
    return BeautifulSoup(content.decode('utf-8'), 'html.parser')


def get_book_info(isbn):
    api_url = 'https://openlibrary.org/search.json?isbn=' + isbn
    response = handle_requests(api_url)
    if response is not None:
        response_json = response.json()
        if response_json['numFound'] > 0:
            book_info = response_json['docs'][0]
            book_info['isbn'] = isbn
            return book_info
    return None


def get_serie_name(url, already_past=False):
    content = handle_requests(url).content
    if content is not None:
        url_parsed = bs_parser(content)
        if not already_past:
            end_url = url_parsed.find(attrs={'class': 'card-link'}).get('href')
            url = 'https://www.bdbase.fr' + end_url
            return get_serie_name(url, already_past=True)
        serie_name = url_parsed.find_all(attrs={'class': 'book-data-summary'})[-1].find('div').text
        return serie_name
    return None
