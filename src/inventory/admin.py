from django.contrib import admin

from .models import ProductGroup, ProductSubGroup, Brand, Warehouse, Product, Extent
# Register your models here.
admin.site.register(ProductGroup)
admin.site.register(Brand)
admin.site.register(Warehouse)
admin.site.register(Product)
admin.site.register(ProductSubGroup)
admin.site.register(Extent)