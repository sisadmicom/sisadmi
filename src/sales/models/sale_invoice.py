from django.db import models
from documents.models.base_document import BaseDocument, BaseDocumentLine
from sri.task import process_invoice


class SaleInvoice(BaseDocument):

    class Meta:
        db_table = "sale_invoice"


class SaleInvoiceLine(BaseDocumentLine):

    document = models.ForeignKey(
        SaleInvoice,
        related_name="lines",
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = "sale_invoice_line"


def calculate_totals(self):

    subtotal = 0

    for line in self.lines.all():
        line.subtotal = line.qty * line.price
        line.save()

        subtotal += line.subtotal

    self.subtotal = subtotal
    self.tax_total = subtotal * 0.15  # IVA Ecuador
    self.total = self.subtotal + self.tax_total

    self.save()

def action_confirm(self):

    self.calculate_totals()

    self.state = "confirmed"
    self.save()

def action_done(self):

    self.state = "done"
    self.save()

    # aquí entra SRI
    
    process_invoice.delay(self.id)

