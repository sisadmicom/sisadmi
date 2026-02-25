#core/urls.py
from django.urls import path, include
from .views import select_context

urlpatterns = [
    path("select-context/", select_context, name="select_context"),
]

urlpatterns = [
    path("select-context/", select_context, name="select_context"),
    path("purchases/", include("purchases.urls")),
]