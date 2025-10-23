from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path
from .models import Company, Branch

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'company']

    
#from django.contrib import admin

#from .models import Company, Branch
# Register your models here.
#admin.site.register(Company)
#admin.site.register(Branch)


