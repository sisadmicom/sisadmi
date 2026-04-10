from django.shortcuts import render

# Create your views here.
# sales/views.py
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import SaleInvoice, SaleInvoiceLine

@csrf_exempt
def create_invoice(request):
    if request.method == "POST":
        data = json.loads(request.body)

        invoice = SaleInvoice.objects.create(
            # ajusta según tu modelo
            customer_name=data.get("customer", "Consumidor Final")
        )

        for line in data.get("lines", []):
            SaleInvoiceLine.objects.create(
                document=invoice,
                product_name=line["product"],
                quantity=line["qty"],
                price=line["price"]
            )

        return JsonResponse({"status": "ok", "invoice_id": invoice.id})