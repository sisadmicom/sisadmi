from django.db import models

from config import settings


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
        #"auth.User",
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="+"
    )

    document_type = models.ForeignKey(
        "documents.DocumentType",
        on_delete=models.PROTECT
    )


    #totales
    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    tax_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )


    #sri
    access_key = models.CharField(        max_length=49,        blank=True,        null=True    )
    xml_signed = models.TextField(        blank=True,        null=True    )
    sri_status = models.CharField(        max_length=20,        blank=True,        null=True    )
    sri_authorization = models.TextField(        blank=True,        null=True    )

    """
    document.xml_signed = signed_xml.decode()
    document.save()
    """
    class Meta:
        abstract = True


class BaseDocumentLine(models.Model):

    document = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    product = models.ForeignKey(
        "inventory.Product",
        verbose_name="Producto",
        on_delete=models.PROTECT
    )
    """product = models.ForeignKey(
        "products.Product",
        on_delete=models.PROTECT
    )
    """

    qty = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)

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


"""
En DocumentServices
subtotal_total = 0
tax_total = 0

for line in lines:

    qty = line["qty"]
    price = line["price"]

    subtotal = qty * price

    tax_amount = TaxService.compute_line_tax(line)

    subtotal_total += subtotal
    tax_total += tax_amount

    document.subtotal = subtotal_total
    document.tax_total = tax_total
    document.total = subtotal_total + tax_total
    document.save()
"""

"""
Ambientes
pruebas
    recepcion:
    https://celcer.sri.gob.ec/comprobantes-electronicos-ws/RecepcionComprobantesOffline?wsdl
    Autorizacion:
    https://celcer.sri.gob.ec/comprobantes-electronicos-ws/AutorizacionComprobantesOffline?wsdl

Produccion
    recepcion:
        https://cel.sri.gob.ec/comprobantes-electronicos-ws/RecepcionComprobantesOffline?wsdl
    Autorizacion: 
        https://cel.sri.gob.ec/comprobantes-electronicos-ws/AutorizacionComprobantesOffline?wsdl   
"""