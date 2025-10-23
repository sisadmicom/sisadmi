from django.urls import path
from .views import select_context

urlpatterns = [
    path("select-context/", select_context, name="select_context"),
]
