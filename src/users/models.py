# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from companies.models import Company, Branch

class User(AbstractUser):
    active_company = models.ForeignKey(
        Company, null=True, blank=True, on_delete=models.SET_NULL, related_name="active_users"
    )
    active_branch = models.ForeignKey(
        Branch, null=True, blank=True, on_delete=models.SET_NULL, related_name="active_users"
    )
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True,related_name="users")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True,related_name="users")
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



class UserCompanyMembership(models.Model):
    ROLE_CHOICES = [
        ("ADMIN", "Administrador"),
        ("STAFF", "Personal"),
        ("VIEWER", "Consulta"),
    ]
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='memberships')
    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='VIEWER')
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'company')
        verbose_name = 'Membresía usuario-empresa'
        verbose_name_plural = 'Membresías usuario-empresa'

    def __str__(self):
        return f"{self.user.username} -> {self.company.name} ({self.role})"
