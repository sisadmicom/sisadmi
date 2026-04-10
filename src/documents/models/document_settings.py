#document_settings.py
from django.db import models


class DocumentSettings(models.Model):

    document_type = models.OneToOneField(
        "documents.DocumentType",
        on_delete=models.CASCADE
    )

    sequence = models.ForeignKey(
        "documents.DocumentSequence",
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    initial_status = models.ForeignKey(
        "documents.DocumentStatus",
        on_delete=models.PROTECT,
        related_name="initial_documents"
    )

    generate_inventory = models.BooleanField(
        default=False
    )

    generate_accounting = models.BooleanField(
        default=False
    )

    electronic = models.BooleanField(
        default=False
    )

    class Meta:
        verbose_name = "Configuración de Documento"
        verbose_name_plural = "Configuraciones de Documento"

    def __str__(self):
        return f"Settings {self.document_type.code}"