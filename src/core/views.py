from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def select_context(request):
    return HttpResponse("Vista de selección de contexto")

# core/views.py
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def test_context(request):
    return Response({
        "active_company": str(getattr(request, "active_company", None)),
        "active_branch": str(getattr(request, "active_branch", None))
    })
