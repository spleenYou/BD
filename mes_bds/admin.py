from django.contrib import admin
from .models import Family, Author, ComicBook, Manga, Book, Library


@admin.register(Family)
class Family(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
    )
    list_filter = (
    )
    list_display_links = (
    )


@admin.register(Author)
class Author(admin.ModelAdmin):
    list_display = (
        'id',
        'lastname',
        'firstname',
    )
    list_filter = (
    )
    list_display_links = (
    )


@admin.register(ComicBook)
class ComicBook(admin.ModelAdmin):
    list_display = (
        'id',
        'number',
        'name',
    )
    list_filter = (
    )
    list_display_links = (
    )


@admin.register(Manga)
class Manga(admin.ModelAdmin):
    list_display = (
        'id',
        'number',
        'name',
    )
    list_filter = (
    )
    list_display_links = (
    )


@admin.register(Book)
class Book(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )
    list_filter = (
    )
    list_display_links = (
    )


@admin.register(Library)
class Library(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
    )
    list_filter = (
    )
    list_display_links = (
    )
