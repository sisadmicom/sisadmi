# core/management/commands/load_initial_data.py

from django.core.management.base import BaseCommand
from companies.models import Company, Branch
#from django.contrib.auth.models import User
from django.db import transaction
from django.contrib.auth import get_user_model
from core.models import MovementFlow
from people.models import Canton, Country, Gender, Parish, Province

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

        #Crear los tipos de movimientos basicos(Inventario inicial)
        type_movement, createdcore = MovementFlow.objects.get_or_create(
            id=1,
            defaults={
                "code": "1",
                "name": "Inventario inicial",
                "title": "INVENTARIO INICIAL",
                "signo": "+",
                "category": "IN",
                "affects_inventory": True,
            },
        )

        #Crear los tipos de movimientos basicos(Ingreso de bodega)
        type_movement, createdcore = MovementFlow.objects.get_or_create(
            id=2,
            defaults={
                "code": "2",
                "name": "Ingreso de bodega",
                "title": "INGRESO DE BODEGA",
                "signo": "+",
                "category": "IN",
                "affects_inventory": True,
            },
        )

        #Crear los tipos de movimientos basicos(Egreso de bodega)
        type_movement, createdcore = MovementFlow.objects.get_or_create(
            id=3,
            defaults={
                "code": "3",
                "name": "Egreso de bodega",
                "title": "EGRESO DE BODEGA",
                "signo": "-",
                "category": "OUT",
                "affects_inventory": True,
            },
        )

        #Crear los tipos de movimientos basicos(Compras)
        type_movement, createdcore = MovementFlow.objects.get_or_create(
            id=4,
            defaults={
                "code": "4",
                "name": "Compras",
                "title": "COMPRAS",
                "signo": "+",
                "category": "IN",
                "affects_inventory": True,
            },
        )

        #Crear los tipos de movimientos basicos(Ventas)
        type_movement, createdcore = MovementFlow.objects.get_or_create(
            id=5,
            defaults={
                "code": "5",
                "name": "Ventas",
                "title": "VENTAS",
                "signo": "-",
                "category": "OUT",
                "affects_inventory": True,
            },
        )
        
        country, createdcore=Country.objects.get_or_create(
            id= 1,
            defaults={
                "name": "ECUADOR",
                "code": "593",
            },
        )
        
        province, createdcore=Province.objects.get_or_create(
            id = 1,
            defaults={
                "country": country,
                "name": "MANABI",
            }
        )

        canton, createdcore=Canton.objects.get_or_create(
            id=1,
            defaults={
                "province": province,
                "name": "PORTOVIEJO",
            }
        )

        parish, createdcore=Parish.objects.get_or_create(
            id=1,
            defaults={
                "canton": canton,
                "name": "ABDON CALDERON",
            }
        )

        gender, createdcore=Gender.objects.get_or_create(
            id=1,
            defaults={
                "name": "MASCULINO",
                "symbol": "H",
            }
        )

        gender, createdcore=Gender.objects.get_or_create(
            id=2,
            defaults={
                "name": "FEMENINO",
                "symbol": "M",
            }
        )


        self.stdout.write("🎉 Datos iniciales cargados exitosamente.!")
        