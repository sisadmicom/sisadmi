# core/models.py
from django.db import models
from django.conf import settings

class BaseModel(models.Model):
    id = models.BigAutoField(primary_key=True)

    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        default=1,
        related_name="%(class)s_records"
    )

    branch = models.ForeignKey(
        'companies.Branch',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        default=1,
        related_name="%(class)s_records"
    )

    # Fechas de auditoría 
    created_at = models.DateTimeField(auto_now_add=True)  # ❌ sin default
    updated_at = models.DateTimeField(auto_now=True)      # ❌ sin default

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_created"
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated"
    )

    class Meta:
        abstract = True
        ordering = ['-created_at']


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class MovementFlow(BaseModel):
    code = models.CharField("Codigo", max_length=5,unique=True)
    name = models.CharField("Nombre", max_length=150)
    title= models.CharField("Tilulo",max_length=150)
    FOW_TYPES = [
        ("+", "(+) el inventario"),
        ("-", "(-) el inventario"),
    ]

    signo = models.CharField(
        max_length=1,default="+",
        choices=FOW_TYPES,
        verbose_name="Suma o Resta"
    )

    FLOW_CATEGORY = [
        ("IN", "Ingreso"),
        ("OUT", "Egreso"),
        ("TR", "Transferencia"),
        ("ADJ", "Ajuste"),
    ]
    category = models.CharField(max_length=4, choices=FLOW_CATEGORY, default="IN")
    affects_inventory = models.BooleanField("Afecta Inventario", default=True)

    class Meta:
        verbose_name = "Flujo de inventario"
        verbose_name_plural = "Flujos de inventario"
        ordering = ["name"]

    def __str__(self):
        return f"{self.code} - {self.name}"
    

class BaseHeader(BaseModel):
    code = models.CharField("Codigo", max_length=5,unique=True)
    flow = models.ForeignKey(MovementFlow, verbose_name="Flujo de inventario", on_delete=models.SET_NULL, null=True)
    document_date = models.DateField("Fecha del documento", auto_now_add=True)
    begin_date = models.DateField("Fecha inicio", blank=True, null=True)
    end_date = models.DateField("Fecha fin", blank=True, null=True)
    reference = models.CharField("Referencia externa", max_length=50, blank=True, null=True)
    STATUS_CHOICES = [
        ("draft", "Borrador"),
        ("confirmed", "Confirmado"),
        ("cancelled", "Anulado"),
    ]
    status = models.CharField(
        "Estado",
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft"
    )
    subtotal = models.DecimalField("Subtotal", max_digits=14, decimal_places=2, default=0)
    discounts = models.DecimalField("Descuentos", max_digits=14, decimal_places=2, default=0)
    zero_tax_base = models.DecimalField("Base sin Impuestos", max_digits=14, decimal_places=2, default=0)
    tax_base = models.DecimalField("Base_Impuestos", max_digits=14, decimal_places=2, default=0)
    total = models.DecimalField("Total", max_digits=14, decimal_places=2, default=0)
    observations = models.TextField("Observaciones", blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.code} - {self.flow}"

class BaseMovements(BaseModel):
    product = models.ForeignKey(
        "inventory.Product",
        verbose_name="Producto",
        on_delete=models.PROTECT
    )
    name = models.CharField("Nombre", max_length=50)
    unit_quantity = models.DecimalField("Cantidad", max_digits=14, decimal_places=2, default=0)
    fraction_quantity = models.DecimalField("Fraccion", max_digits=14, decimal_places=2, default=0)
    unit_value = models.DecimalField("Valor Unitario", max_digits=14, decimal_places=2, default=0)
    fraction_value = models.DecimalField("Valor Fraccion", max_digits=14, decimal_places=2, default=0)
    discounts = models.DecimalField("Descuentos", max_digits=14, decimal_places=2, default=0)
    taxes = models.DecimalField("Impuestos", max_digits=14, decimal_places=2, default=0)
    #product = models.ForeignKey("products.Product", on_delete=models.PROTECT)
    
    class Meta:
        abstract = True
        ordering = ['id']

    @property
    def line_total(self):
        return (self.unit_quantity * self.unit_value) - self.discounts + self.taxes

    def __str__(self):
        return f"{self.product} - {self.unit_quantity} u."
