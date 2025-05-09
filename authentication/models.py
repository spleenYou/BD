from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    birthday = models.DateField(
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Liste d\'utilisateur'
        verbose_name_plural = 'Liste des utilisateurs'
