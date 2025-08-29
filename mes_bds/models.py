from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator


class TimestampedModel(models.Model):
    time_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date de création',
    )
    time_updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Date de mise à jour',
    )

    class Meta:
        abstract = True


class Family(TimestampedModel):
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


class Author(TimestampedModel):
    name = models.CharField(
        max_length=255,
        null=False,
        verbose_name='Nom de l\'auteur',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Auteurs'


class Artist(TimestampedModel):
    name = models.CharField(
        max_length=255,
        null=False,
        verbose_name='Nom de l\'artiste',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Artistes'


class Publisher(TimestampedModel):
    name = models.CharField(
        max_length=255,
        null=False,
        verbose_name='Nom de l\'éditeur',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Editeurs'


class Serie(TimestampedModel):
    name = models.CharField(
        max_length=255,
        null=False,
        verbose_name='Nom de la série',
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Description'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Séries'


class Book(TimestampedModel):
    title = models.CharField(
        max_length=128,
    )
    ISBN_10 = models.CharField(
        null=True,
        blank=True,
        max_length=10,
        validators=[MinLengthValidator(10)],
        verbose_name='ISBN-10'
    )
    ISBN_13 = models.CharField(
        null=True,
        blank=True,
        max_length=13,
        validators=[MinLengthValidator(13)],
        verbose_name='ISBN-13'
    )
    number = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name='Numéro',
    )
    author = models.ForeignKey(
        Author,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='books',
        verbose_name='Auteur',
    )
    artist = models.ForeignKey(
        Artist,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='books',
        verbose_name='Artiste',
    )
    serie = models.ForeignKey(
        Serie,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='books',
        verbose_name='Série',
    )
    publisher = models.ForeignKey(
        Publisher,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='books',
        verbose_name='Editeur'
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
        default='BD',
    )
    description = models.TextField(
        null=True,
        blank=True,
    )
    cover_ID = models.CharField(
        null=True,
        blank=True,
        max_length=20,
        verbose_name='ID de couverture',
    )

    def __str__(self):
        if self.serie and self.number:
            return f"{self.serie.name} - Tome {self.number} {self.title}"
        return self.title

    class Meta:
        verbose_name_plural = "Livres"
        indexes = [
                models.Index(fields=['book_type']),
                models.Index(fields=['title']),
            ]


class Library(TimestampedModel):
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
        verbose_name='Livre',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'book_list'],
                name='unique_user_book'
            )
        ]
        verbose_name_plural = "Bibliothèques"
