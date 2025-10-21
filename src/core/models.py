# core/models.py
from django.db import models
from django.conf import settings

class BaseModel(models.Model):
    id = models.BigAutoField(primary_key=True)

    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="%(class)s_records"
    )

    # Fechas de auditoría
    created_at = models.DateTimeField(auto_now_add=True)  # ❌ sin default
    updated_at = models.DateTimeField(auto_now=True)      # ❌ sin default

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_created"
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated"
    )

    class Meta:
        abstract = True
        ordering = ['-created_at']


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True