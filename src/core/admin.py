from django.contrib import admin
from companies.models import Company, Branch

# ⚠️ No registramos Branch aquí porque ya está registrado en companies/admin.py
# y Django no permite registrar el mismo modelo dos veces.

# Si necesitas usar Branch dentro del admin (por ejemplo, para lógica interna),
# puedes accederlo directamente sin registrarlo, así:
# branches = Branch.objects.all()

# Este archivo debe contener solo clases y registros de admin, no rutas ni vistas.
# Por ejemplo, si tuvieras modelos propios de 'core', se verían así:

# from .models import SomeCoreModel
# @admin.register(SomeCoreModel)
# class SomeCoreModelAdmin(admin.ModelAdmin):
#     list_display = ("name", "created_at")

# Fin del archivo admin.py
