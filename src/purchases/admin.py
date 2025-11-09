from django.contrib import admin

from .models import PurchaseHeader, PurchaseMovement
admin.site.register(PurchaseHeader)
admin.site.register(PurchaseMovement)