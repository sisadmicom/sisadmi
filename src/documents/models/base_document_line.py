#/home/sisadmi/workspace/sisadmi/src/documents/models/base_document_line.py
from django.db import models

class BaseDocumentLine(models.Model):

    product = models.ForeignKey(
        "inventory.Product",
        on_delete=models.PROTECT
    )

    description = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    qty = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        abstract = True

    def calculate_subtotal(self):
        self.subtotal = self.qty * self.price