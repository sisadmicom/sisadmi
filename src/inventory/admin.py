from django.contrib import admin

from .models import ProductGroup, Brand, Warehouse, Product
# Register your models here.
admin.site.register(ProductGroup)
admin.site.register(Brand)
admin.site.register(Warehouse)
admin.site.register(Product)