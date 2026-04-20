#/home/sisadmi/workspace/sisadmi/src/sales/views.py
from django.shortcuts import render, redirect
from inventory.models import Product
from people.models import Person
from .models import SaleInvoice, SaleInvoiceLine
from django.shortcuts import get_object_or_404

def invoice_create(request):

    products = Product.objects.all()
    customers = Person.objects.all()

    if request.method == "POST":

        customer_id = request.POST.get("customer")

        invoice = SaleInvoice.objects.create(
            customer_id=customer_id,
            company_id=1,
            document_type_id=1,
            date="2026-01-01",
            created_by=request.user
        )

        # Crear líneas correctamente
        product_ids = request.POST.getlist("product[]")
        qtys = request.POST.getlist("qty[]")
        prices = request.POST.getlist("price[]")

        for i in range(len(product_ids)):
            SaleInvoiceLine.objects.create(
                invoice=invoice,
                #invoice=invoice,  # ✅ CORRECTO
                product_id=product_ids[i],
                qty=qtys[i],
                price=prices[i],
            )

        invoice.calculate_totals()

        # 🔥 REDIRECCIÓN CLAVE
        return redirect("invoice_detail", pk=invoice.id)

    return render(request, "sales/invoice/invoice_form.html", {
        "products": products,
        "customers": customers,
    })


from django.shortcuts import get_object_or_404

def invoice_detail(request, pk):
    invoice = get_object_or_404(SaleInvoice, pk=pk)

    return render(request, "sales/invoice/invoice_detail.html", {
        "invoice": invoice
    })

from django.views.decorators.http import require_POST

@require_POST
def invoice_confirm(request, pk):
    invoice = get_object_or_404(SaleInvoice, pk=pk)
    invoice.action_confirm()
    return redirect("invoice_detail", pk=pk)


@require_POST
def invoice_post(request, pk):
    invoice = get_object_or_404(SaleInvoice, pk=pk)
    invoice.action_post()
    return redirect("invoice_detail", pk=pk)