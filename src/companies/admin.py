from django.contrib import admin
from .models import Company
from .models import Branch

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("person", "trade_name", "website")
#, "created_at", "updated_at"
admin.site.register(Branch)
