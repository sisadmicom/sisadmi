from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def select_context(request):
    return HttpResponse("Vista de selección de contexto")
