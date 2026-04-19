#/home/sisadmi/workspace/sisadmi/src/sales/models/sale_invoice.py
from django.db import models
from documents.models.base_document import BaseDocument
from documents.models.base_document_line import BaseDocumentLine

#IVA_RATE = 0.15  # Ecuador
from decimal import Decimal

IVA_RATE = Decimal("0.15")

class SaleInvoice(BaseDocument):

    customer = models.ForeignKey(
        "people.Person",
        on_delete=models.PROTECT,
        related_name="sale_invoices"
    )

    class Meta:
        db_table = "sale_invoice"

    # 🧠 Lógica central tipo Odoo
    def calculate_totals(self):

        subtotal = 0

        #for line in self.lines.all():
        for line in self.lines.select_related("product"):
            line.calculate_subtotal()
            line.save()
            subtotal += line.subtotal

        self.subtotal = subtotal
        self.tax_total = subtotal * IVA_RATE
        self.total = self.subtotal + self.tax_total

        self.save()

    # 🚀 Acciones
    def action_confirm(self):
        self.calculate_totals()
        self.status = "confirmed"
        self.save()

    def action_post(self):
        self.status = "posted"
        self.save()

        # Enviar a SRI async
        from sri.task import process_invoice
        process_invoice.delay(self.id)