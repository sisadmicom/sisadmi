#purchases/models.py
from django.db import models
from core.models import BaseHeader, BaseMovements

class PurchaseHeader(BaseHeader):
    supplier = models.ForeignKey("people.Person", on_delete=models.PROTECT, verbose_name="Proveedor")
    invoice_number = models.CharField("Número de factura", max_length=30)

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"

    def __str__(self):
        return f"Compra {self.code} - {self.supplier}"


class PurchaseMovement(BaseMovements):
    header = models.ForeignKey(PurchaseHeader, related_name="movements", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Detalle de Compra"
        verbose_name_plural = "Detalles de Compra"

