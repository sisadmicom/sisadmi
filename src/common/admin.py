from django.contrib import admin

from .models import BaseModel, TimeStampedModel
# Register your models here.
admin.site.register(BaseModel)
admin.site.register(TimeStampedModel)