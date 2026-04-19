#/home/sisadmi/workspace/sisadmi/src/documents/models/base_document.py
from django.db import models
from django.conf import settings


class BaseDocument(models.Model):

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("confirmed", "Confirmed"),
        ("posted", "Posted"),
        ("cancelled", "Cancelled"),
    ]

    company = models.ForeignKey(
        "companies.Company",
        on_delete=models.PROTECT
    )

    document_type = models.ForeignKey(
        "documents.DocumentType",
        on_delete=models.PROTECT
    )

    number = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )

    date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft"
    )

    notes = models.TextField(blank=True, null=True)

    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="+"
    )

    # Totales
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # SRI
    access_key = models.CharField(max_length=49, blank=True, null=True)
    xml_signed = models.TextField(blank=True, null=True)
    sri_status = models.CharField(max_length=20, blank=True, null=True)
    sri_authorization = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True

    # 🔢 Generación de número
    def generate_number(self):
        if self.number:
            return

        if self.document_type and self.document_type.sequence:
            self.number = self.document_type.sequence.next_number()

    def save(self, *args, **kwargs):
        if not self.number:
            self.generate_number()

        super().save(*args, **kwargs)