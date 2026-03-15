from django.shortcuts import render

# Create your views here.
from documents.services.document_service import DocumentService
from documents.models import DocumentType


def create_sale(request):

    document_type = DocumentType.objects.get(code="sale_order")

    lines = [
        {
            "product": product1,
            "qty": 2,
            "price": 10
        },
        {
            "product": product2,
            "qty": 1,
            "price": 50
        }
    ]

    doc = DocumentService.create_document(
        document_type=document_type,
        partner=customer,
        lines=lines
    )