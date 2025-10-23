# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from companies.models import Company, Branch

class User(AbstractUser):
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True,related_name="companyes")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True,related_name="branchs")
    '''company = models.ForeignKey(
        'companies.Company',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users"
    )'''

    person = models.OneToOneField(
        'people.Person',
        on_delete=models.CASCADE,
        related_name='user_account',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.username} ({self.company})" if self.company else self.username
