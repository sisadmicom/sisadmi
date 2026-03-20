from django.db import models


class Tax(models.Model):

    code = models.CharField(
        max_length=20,
        unique=True
    )

    name = models.CharField(
        max_length=100
    )

    rate = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.name} ({self.rate}%)"
    """
    Asociar impuestos a lineas de documentos
    tax = models.ForeignKey(
        "accounting.Tax",
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    tax_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )
    """