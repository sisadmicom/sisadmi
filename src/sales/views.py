import json
from django.shortcuts import render, redirect
from inventory.models import Product
from people.models import Person
from .models import SaleInvoice, SaleInvoiceLine

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

        # Procesar líneas
        for i in range(len(request.POST.getlist("product[]"))):
            SaleInvoiceLine.objects.create(
                document=invoice,
                product_id=request.POST.getlist("product[]")[i],
                qty=request.POST.getlist("qty[]")[i],
                price=request.POST.getlist("price[]")[i],
            )

        invoice.calculate_totals()

        return redirect("invoice_list")

    products_json = json.dumps([
        {"id": p.id, "name": p.name, "price": float(p.price)}
        for p in products
    ])
    #/home/sisadmi/workspace/sisadmi/src/sales/templates/sales/invoice/invoice_form.html
    return render(request, "sales/invoice/invoice_detail.html", {
        "invoice": invoice
    })
    """return render(request, "sales/invoice_form.html", {
        "products": products,
        "customers": customers,
        "products_json": products_json
    })"""