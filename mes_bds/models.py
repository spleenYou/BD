from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


class Family(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='family_maker',
        verbose_name='utilisateur'
    )
    family_member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='family_member',
        verbose_name='Membre de la famille'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'family_member'),
                name='unique_user_user'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('family_member')),
                name='user_not_equal_to_family_member'
            )
        ]
        verbose_name_plural = "Membres de la famille"


class Author(models.Model):
    firstname = models.CharField(
        max_length=20
    )
    lastname = models.CharField(
        max_length=30
    )

    class Meta:
        verbose_name_plural = 'Auteurs'


class ComicBook(models.Model):
    name = models.CharField(
        max_length=128,
    )
    number = models.SmallIntegerField(
        validators=[MinValueValidator(1)],
    )
    author = models.ForeignKey(
        Author,
        null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name_plural = "Bandes dessinees"


class Manga(models.Model):
    name = models.CharField(
        max_length=64
    )
    number = models.SmallIntegerField(
        validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name_plural = "Mangas"


class Book(models.Model):
    name = models.CharField(
        max_length=64
    )
    author = models.ForeignKey(
        Author,
        null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name_plural = "Livres"


class Library(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='Owner',
        verbose_name='Proprietaire'
    )
    comic_book_list = models.ForeignKey(
        ComicBook,
        on_delete=models.CASCADE,
        related_name='comic_book',
        verbose_name='Bande dessinee'
    )
    manga_list = models.ForeignKey(
        Manga,
        on_delete=models.CASCADE,
        related_name='manga',
        verbose_name='Manga'
    )
    book_list = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='book',
        verbose_name='Livre'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'comic_book_list'],
                name='unique_user_comic'
            ),
            models.UniqueConstraint(
                fields=['user', 'manga_list'],
                name='unique_user_manga'
            ),
            models.UniqueConstraint(
                fields=['user', 'book_list'],
                name='unique_user_book'
            )
        ]
        verbose_name_plural = "Bibliothèques"
