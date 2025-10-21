# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users"
    )

    person = models.OneToOneField(
        'people.Person',
        on_delete=models.CASCADE,
        related_name='user_account',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.username} ({self.company})" if self.company else self.username
