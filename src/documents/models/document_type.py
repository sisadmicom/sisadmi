from django.db import models


class DocumentType(models.Model):

    code = models.CharField(
        max_length=20,
        unique=True
    )

    name = models.CharField(
        max_length=100
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    use_sequence = models.BooleanField(
        default=True
    )

    sequence = models.ForeignKey(
        "documents.DocumentSequence",
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    active = models.BooleanField(
        default=True
    )

    class Meta:
        verbose_name = "Tipo de Documento"
        verbose_name_plural = "Tipos de Documento"

    def __str__(self):
        return self.name