from django.contrib import admin
from .models import Family, Author, Book, Library


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


@admin.register(Book)
class Book(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'number',
        'serie',
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
