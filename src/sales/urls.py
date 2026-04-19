# sales/urls.py
from django.urls import path
from .views import invoice_create,SaleInvoiceLine

urlpatterns = [
    path("invoice/create/", invoice_create, name="invoice_create"),
]
urlpatterns = [
    path("invoice/<int:pk>/", SaleInvoiceLine, name="invoice_detail"),
]
#path("api/invoice/", invoice_create),