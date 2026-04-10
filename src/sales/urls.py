# sales/urls.py
from django.urls import path
from .views import create_invoice

urlpatterns = [
    path("api/invoice/", create_invoice),
]