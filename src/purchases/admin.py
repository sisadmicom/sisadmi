from django.contrib import admin

from .models import PurchaseHeader, PurchaseMovement, Supplier
admin.site.register(PurchaseHeader)
admin.site.register(PurchaseMovement)
admin.site.register(Supplier)