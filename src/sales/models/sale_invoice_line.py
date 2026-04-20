from django.db import models
from documents.models.base_document_line import BaseDocumentLine
from .sale_invoice import SaleInvoice


class SaleInvoiceLine(BaseDocumentLine):

    """document = models.ForeignKey(
        SaleInvoice,
        related_name="document_lines",
        on_delete=models.CASCADE
    )"""

    invoice = models.ForeignKey(
        SaleInvoice,
        on_delete=models.CASCADE,
        related_name="lines"
    )

    class Meta:
        db_table = "sale_invoice_line"