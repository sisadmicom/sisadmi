from django.contrib import admin

from .models import ProductGroup, ProductSubGroup, Brand, Warehouse, Product, Extent, Hanger
#from .models import InventoryFow, StockMovement, StockMovementLine, StockItem
admin.site.register(ProductGroup)
admin.site.register(Brand)
admin.site.register(Warehouse)
admin.site.register(Product)
admin.site.register(ProductSubGroup)
admin.site.register(Extent)
admin.site.register(Hanger)
#admin.site.register(InventoryFow)
#admin.site.register(StockMovement)
#admin.site.register(StockMovementLine)
#admin.site.register(StockItem)