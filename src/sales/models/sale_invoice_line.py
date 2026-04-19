from django.db import models
from documents.models.base_document_line import BaseDocumentLine
from .sale_invoice import SaleInvoice


class SaleInvoiceLine(BaseDocumentLine):

    document = models.ForeignKey(
        SaleInvoice,
        related_name="lines",
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = "sale_invoice_line"