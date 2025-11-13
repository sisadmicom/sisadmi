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
    