from django.contrib import admin
from .models import DocumentType, DocumentSequence, DocumentStatus, DocumentSettings, DocumentWorkflow


admin.site.register(DocumentType)
admin.site.register(DocumentSequence)
admin.site.register(DocumentStatus)
admin.site.register(DocumentSettings)
admin.site.register(DocumentWorkflow)