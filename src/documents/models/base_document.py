from django.db import models


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

    number = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )

    date = models.DateField()

    status = models.ForeignKey(
        "documents.DocumentStatus",
        on_delete=models.PROTECT
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    created_by = models.ForeignKey(
        "auth.User",
        on_delete=models.PROTECT,
        related_name="+"
    )

    document_type = models.ForeignKey(
        "documents.DocumentType",
        on_delete=models.PROTECT
    )

    class Meta:
        abstract = True

def generate_number(self):

    if self.number:
        return

    if self.document_type.sequence:

        self.number = self.document_type.sequence.next_number()

def save(self, *args, **kwargs):

    if not self.number:
        self.generate_number()

    super().save(*args, **kwargs)