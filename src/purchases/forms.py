from django import forms
from django.forms import inlineformset_factory
from .models import PurchaseHeader, PurchaseMovement

class PurchaseHeaderForm(forms.ModelForm):
    class Meta:
        model = PurchaseHeader
        fields = ["supplier", "invoice_number", "begin_date"]

class PurchaseMovementForm(forms.ModelForm):
    class Meta:
        model = PurchaseMovement
        fields = ["name", "unit_quantity", "unit_value"]

PurchaseFormSet = inlineformset_factory(
    PurchaseHeader,
    PurchaseMovement,
    form=PurchaseMovementForm,
    extra=1,
    can_delete=True
)