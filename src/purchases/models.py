#purchases/models.py
from django.db import models
from core.models import BaseHeader, BaseModel, BaseMovements
from people.models import Person

class Supplier(BaseModel):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, related_name="supplier_profile")
    contact_person = models.CharField(max_length=150, blank=True)
    caducidad = models.DateField("Fecha del caducidad", auto_now_add=True)
    establecimiento = models.CharField("establecimiento", max_length=3, blank=True, null=True)
    punto = models.CharField("Punto de emisiòn", max_length=3, blank=True, null=True)
    count = models.CharField("Cuenta contable", max_length=15, blank=True, null=True)
    web = models.CharField("Pagina web", max_length=50, blank=True, null=True)
    class Meta:
        db_table = "purchases_supplier"  # 👈 usa el nombre de la tabla original
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"

    def __str__(self):
        return str(self.person)
    
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

