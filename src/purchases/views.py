from django.shortcuts import get_object_or_404, render
from .models import PurchaseHeader

def purchase_document(request, pk):
    purchase = get_object_or_404(PurchaseHeader, pk=pk)
    return render(request, "purchases/document.html", {
        "purchase": purchase
    })


from django.shortcuts import render, redirect
from django.utils import timezone
from .models import PurchaseHeader
from .forms import PurchaseHeaderForm, PurchaseFormSet

def purchase_create(request):
    if request.method == "POST":
        form = PurchaseHeaderForm(request.POST)
        formset = PurchaseFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            purchase = form.save()
            formset.instance = purchase
            formset.save()
            return redirect("purchases/document.html", pk=purchase.pk)
    else:
        form = PurchaseHeaderForm(initial={
            "date": timezone.now().date()
        })
        formset = PurchaseFormSet()

    return render(request, "purchases/create.html", {
        "form": form,
        "formset": formset
    })