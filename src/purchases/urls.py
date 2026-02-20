from django.urls import path
from . import views

urlpatterns = [
    path("document/<int:pk>/", views.purchase_document, name="purchase_document"),
]
