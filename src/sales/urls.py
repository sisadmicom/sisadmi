from django.urls import path
from .views import invoice_create, invoice_detail, invoice_confirm, invoice_post

urlpatterns = [
    path("invoice/create/", invoice_create, name="invoice_create"),
    path("invoice/<int:pk>/", invoice_detail, name="invoice_detail"),

    # 🔥 acciones ERP
    path("invoice/<int:pk>/confirm/", invoice_confirm, name="invoice_confirm"),
    path("invoice/<int:pk>/post/", invoice_post, name="invoice_post"),
]