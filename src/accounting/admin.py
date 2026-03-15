from django.contrib import admin

from .models import Account,Project,CostCenter
# Register your models here.
admin.site.register(Account)
admin.site.register(Project)
admin.site.register(CostCenter)