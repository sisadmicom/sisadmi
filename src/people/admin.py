from django.contrib import admin
from django import forms
#from .models import Person

#from django.contrib import admin
from .models import Country, Province, Canton, Parish, Person, Gender, Employee
# Register your models here.
admin.site.register(Country)
admin.site.register(Province)
admin.site.register(Canton)
admin.site.register(Parish)
admin.site.register(Gender)
admin.site.register(Employee)

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = "__all__"

    class Media:
        js = ('js/person_admin.js',)  # ← este archivo lo crearás en el siguiente paso


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    form = PersonForm
    list_display = ('identification', 'person_type', 'name', 'last_name', 'company_name')

    # Esto ayuda a mantener los campos agrupados
    fieldsets = (
        (None, {
            'fields': ('person_type', 'identification', 'name', 'last_name', 'company_name')
        }),
        ('Información adicional', {
            'fields': ('email', 'birth_date', 'gender', 'parish', 'phone')
        }),
    )