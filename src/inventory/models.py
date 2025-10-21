from core import models
from core.models import BaseModel


class ProductGroup(BaseModel):
    name = models.CharField(max_length=100)

class Brand(BaseModel):
    name = models.CharField(max_length=100)

class Warehouse(BaseModel):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=150, blank=True, null=True)

class Product(BaseModel):
    code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=150)
    group = models.ForeignKey(ProductGroup, on_delete=models.SET_NULL, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True)
