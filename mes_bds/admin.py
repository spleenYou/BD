from django.contrib import admin
from .models import Family, Author, Artist, Publisher, Serie, Book, Library


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
        'name',
    )
    list_filter = (
    )
    list_display_links = (
    )


@admin.register(Artist)
class Artist(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )
    list_filter = (
    )
    list_display_links = (
    )


@admin.register(Publisher)
class Publisher(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )
    list_filter = (
    )
    list_display_links = (
    )


@admin.register(Serie)
class Serie(admin.ModelAdmin):
    list_display = (
        'id',
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
        'serie',
        'number',
        'title',
        'book_type',
    )
    list_filter = (
        'serie',
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
