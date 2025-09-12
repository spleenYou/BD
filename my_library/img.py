from django.core.files.base import ContentFile
import requests


def save_book_cover(instance, cover_id):
    url = 'https://covers.openlibrary.org/b/olid/'
    filename = cover_id + '-M.jpg'
    resp = requests.get(url + filename)
    if resp.status_code == 200:
        instance.cover.save(filename, ContentFile(resp.content), save=True)
