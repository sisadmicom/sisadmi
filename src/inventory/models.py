from django.db import models      # 👈 siempre primero
from core.models import BaseModel
from companies.models import Company, Branch 

class ProductGroup(BaseModel):
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = "Grupo"
        verbose_name_plural = "Grupos"
        ordering = ["name"]

    def __str__(self):
        return self.name
    
class ProductSubGroup(BaseModel):
    name = models.CharField("Subgrupo", max_length=100, unique=True)
    ProductGroup = models.ForeignKey(ProductGroup, verbose_name="Grupo", on_delete=models.SET_NULL, null=True)  

    class Meta:
        verbose_name = "SubGrupo"
        verbose_name_plural = "SubGrupos"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.ProductGroup})"


#Marcas
class Brand(BaseModel):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"
        ordering = ["name"]

    def __str__(self):
        return self.name

class Warehouse(BaseModel):
    name = models.CharField(max_length=100, verbose_name="Nombre del almacen")
    location = models.CharField(max_length=150, verbose_name="Ubicacion",blank=True, null=True)

    class Meta:
        verbose_name = "Almacen"
        verbose_name_plural = "Almacenes"
        ordering = ["name"]

    def __str__(self):
        return self.name

class Hanger(BaseModel):
    name = models.CharField("Percha" ,max_length=100)
    Warehouse = models.ForeignKey(Warehouse, verbose_name="Almacen", on_delete=models.SET_NULL, null=True) 

    class Meta:
        verbose_name = "Percha"
        verbose_name_plural = "Perchas"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.Warehouse})"


class Extent(BaseModel):
    name = models.CharField("Medida", max_length=100, unique=True)
    symbol = models.CharField("Simbolo", max_length=3,blank=True, null=True)

    class Meta:
        verbose_name = "Medida"
        verbose_name_plural = "Medidas"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} - {self.symbol}"
    

class Product(BaseModel):
    code = models.CharField("Codigo", max_length=30, unique=True)
    name = models.CharField("Nombre", max_length=150)
    group = models.ForeignKey(ProductGroup, verbose_name="Grupo", on_delete=models.SET_NULL, null=True)
    subgroup = models.ForeignKey(ProductSubGroup, verbose_name="Subgrupo", on_delete=models.SET_NULL, null=True )
    brand = models.ForeignKey(Brand, verbose_name="Marca", on_delete=models.SET_NULL, null=True)
    price = models.DecimalField("Precio", max_digits=10, decimal_places=2)
    stock = models.DecimalField("Stop", max_digits=10, decimal_places=2, default=0)
    extent = models.ForeignKey(Extent, verbose_name="Medida", on_delete=models.SET_NULL, null=True)
    warehouse = models.ForeignKey(Warehouse, verbose_name="Almacen", on_delete=models.SET_NULL, null=True)  
    Hanger = models.ForeignKey(Hanger, verbose_name="Percha", on_delete=models.SET_NULL, null=True)
    #company = models.ForeignKey(Company, verbose_name="Empresa", on_delete=models.SET_NULL, null=True, blank=True,related_name="products")
    #branch = models.ForeignKey(Branch, verbose_name="Sucursal", on_delete=models.SET_NULL, null=True, blank=True,related_name="products")

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ["name"]

    def __str__(self):
        return f"{self.code} - {self.name}"
    
"""
class InventoryFow(BaseModel):
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
    #signo= models.CharField("Signo",max_length=150)

    class Meta:
        verbose_name = "Flujo de inventario"
        verbose_name_plural = "Flujos de inventario"
        ordering = ["name"]

    def __str__(self):
        return f"{self.code} - {self.name}"

class StockMovement(BaseModel):
    
    #tipo = models.ForeignKey(InventoryFow, related_name="lines", on_delete=models.CASCADE)
    referencia = models.CharField(max_length=100, blank=True, null=True)  # Ej: factura, compra, nota
    origen = models.ForeignKey(
        Warehouse, related_name="movimientos_origen",
        on_delete=models.SET_NULL, null=True, blank=True
    )
    destino = models.ForeignKey(
        Warehouse, related_name="movimientos_destino",
        on_delete=models.SET_NULL, null=True, blank=True
    )
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Movimiento de Inventario"
        verbose_name_plural = "Movimientos de Inventario"

    def __str__(self):
        return f"{self.tipo} - {self.origen} - {self.destino or 'Sin referencia'}"

class StockMovementLine(models.Model):
    movimiento = models.ForeignKey(StockMovement, related_name="lines", on_delete=models.CASCADE)
    producto = models.ForeignKey(Product, on_delete=models.PROTECT)
    cantidad = models.DecimalField(max_digits=14, decimal_places=4)

    costo_unitario = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.costo_unitario
        super().save(*args, **kwargs)
        # Actualizar el stock
        self.update_stock()

    def update_stock(self):
        
        Actualiza el stock del producto en el almacén correspondiente
        según si es entrada o salida.
        
        if self.movimiento.tipo == InventoryFow.code:
            StockItem.objects.update_or_create(
                producto=self.producto,
                bodega=self.movimiento.destino,
                defaults={"cantidad": models.F("cantidad") + self.cantidad},
            )
        elif self.movimiento.tipo == InventoryFow.code:
            StockItem.objects.update_or_create(
                producto=self.producto,
                bodega=self.movimiento.origen,
                defaults={"cantidad": models.F("cantidad") - self.cantidad},
            )
        # para transfer y adjustment puedes afinar la lógica

class StockItem(models.Model):
    producto = models.ForeignKey(Product, on_delete=models.CASCADE)
    bodega = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=14, decimal_places=4, default=0)

    class Meta:
        unique_together = ("producto", "bodega")
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"

    def __str__(self):
        return f"{self.producto} @ {self.bodega}: {self.cantidad}"
"""

"""
class StockMovementLineInline(admin.TabularInline):
    model = StockMovementLine
    extra = 1

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ("tipo", "fecha", "referencia", "company")
    inlines = [StockMovementLineInline]

@admin.register(StockItem)
class StockItemAdmin(admin.ModelAdmin):
    list_display = ("producto", "bodega", "cantidad")
    """