from django.db import models


class DocumentStatus(models.Model):

    code = models.CharField(
        max_length=20,
        unique=True
    )

    name = models.CharField(
        max_length=100)

    description = models.TextField(
        blank=True,
        null=True
    )

    is_initial = models.BooleanField(
        default=False
    )

    is_final = models.BooleanField(
        default=False
    )

    class Meta:
        verbose_name = "Estado de Documento"
        verbose_name_plural = "Estados de Documento"

    def __str__(self):
        return self.name