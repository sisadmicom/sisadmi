from django.shortcuts import get_object_or_404, render
from .models import PurchaseHeader

def purchase_document(request, pk):
    purchase = get_object_or_404(PurchaseHeader, pk=pk)
    return render(request, "purchases/document.html", {
        "purchase": purchase
    })
