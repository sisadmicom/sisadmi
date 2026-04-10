from django.db import models


class BaseDocumentLine(models.Model):

    """product = models.ForeignKey(
        "products.Product",
        on_delete=models.PROTECT
    )"""
    product = models.ForeignKey(
        "inventory.Product",
        verbose_name="Producto",
        on_delete=models.PROTECT
    )

    quantity = models.DecimalField(
        max_digits=14,
        decimal_places=4
    )

    class Meta:
        abstract = True