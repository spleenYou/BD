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
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date de création'
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
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date de création'
    )

    class Meta:
        verbose_name_plural = 'Auteurs'


class Book(models.Model):
    name = models.CharField(
        max_length=128,
    )
    number = models.SmallIntegerField(
        null=True,
        validators=[MinValueValidator(1)],
    )
    author = models.ForeignKey(
        Author,
        null=True,
        on_delete=models.SET_NULL
    )
    BOOK_TYPES = {
        'BD': 'Bande dessinée',
        'MA': 'Manga',
        'RO': 'Roman',
        'LJ': 'Livre jeunesse',
        'LP': 'Livre pratique',
        'LD': 'Livre documentaire',
        'MS': 'Manuel scolaire',
        'RP': 'Recueil poésie',
        'PT': 'Pièce de théâtre',
        'ES': 'Essai',
        'BI': 'Biographie',
        'AU': 'Autobiographie',
        'LA': 'Livre d\'art',
    }
    book_type = models.CharField(
        max_length=2,
        choices=BOOK_TYPES,
        default='BD'
    )
    description = models.CharField(
        null=True
    )
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date de création'
    )

    class Meta:
        verbose_name_plural = "Bandes dessinees"


class Library(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='Owner',
        verbose_name='Proprietaire'
    )
    book_list = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='book',
        verbose_name='Livre'
    )
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date de création'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'book_list'],
                name='unique_user_book'
            )
        ]
        verbose_name_plural = "Bibliothèques"
