import requests


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
