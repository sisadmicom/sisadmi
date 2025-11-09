# core/management/commands/load_initial_data.py

from django.core.management.base import BaseCommand
from companies.models import Company, Branch
#from django.contrib.auth.models import User
from django.db import transaction
from django.contrib.auth import get_user_model
User = get_user_model()

class Command(BaseCommand):
    help = "Carga datos base iniciales (empresa, sucursal, usuario admin, etc.)"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("🚀 Iniciando carga de datos base...")

        # 2️⃣ Crear o asegurar la sucursal base (sin empresa aún)
        branch, created_branch = Branch.objects.get_or_create(
            #code="001",
            id = 1,
            defaults={
                "name": "Matriz",
                "address": "Dirección principal",
                "company": None,  # <-- importante
                #"company_id": None,
            },
        )

        # 1️⃣ Crear empresa base (asociada a la sucursal)
        company, created_company = Company.objects.get_or_create(
            #code="001",
            id = 1,
            defaults={
                "name": "Empresa Principal",
                "ruc": "9999999999999",
                "branch": branch,  # <-- ahora ya existe la sucursal
                #"company_id": None,
            },
        )
        
       

        # 3️⃣ Actualizar sucursal con empresa
        if branch.company is None:
            branch.company = company
            branch.save()

        # 4️⃣ Crear usuario administrador
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "sis@dmi.com", "admin123")
            self.stdout.write("✅ Usuario admin creado.")

        self.stdout.write("🎉 Datos iniciales cargados exitosamente.")
