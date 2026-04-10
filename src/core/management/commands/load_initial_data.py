# core/management/commands/load_initial_data.py

from django.core.management.base import BaseCommand
from companies.models import Company, Branch
#from django.contrib.auth.models import User
from django.db import transaction
from django.contrib.auth import get_user_model
from core.models import MovementFlow
from people.models import Canton, Country, Gender, Parish, Province
from documents.models import DocumentSettings,DocumentType,DocumentWorkflow,DocumentStatus,DocumentSequence
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


        # =========================
        # 1. ESTADOS
        # =========================
        statuses_data = [
            ("draft", "Borrador", True, False),
            ("posted", "Publicado", False, False),
            ("done", "Finalizado", False, True),
            ("cancelled", "Anulado", False, True),
        ]

        status_map = {}

        for code, name, is_initial, is_final in statuses_data:
            status, _ = DocumentStatus.objects.get_or_create(
                code=code,
                defaults={
                    "name": name,
                    "is_initial": is_initial,
                    "is_final": is_final,
                }
            )
            status_map[code] = status

        self.stdout.write(self.style.SUCCESS("✅ Estados creados"))

        # =========================
        # 2. TIPOS DE DOCUMENTO
        # =========================
        document_types_data = [
            ("INV", "Factura"),
            ("NCR", "Nota de Crédito"),
            ("BILL", "Factura de Compra"),
            ("IN", "Ingreso de Inventario"),
            ("OUT", "Egreso de Inventario"),
        ]

        doc_type_map = {}

        for code, name in document_types_data:
            doc_type, _ = DocumentType.objects.get_or_create(
                code=code,
                defaults={"name": name}
            )
            doc_type_map[code] = doc_type

        self.stdout.write(self.style.SUCCESS("✅ Tipos de documento creados"))

        # =========================
        # 3. CONFIGURACIONES
        # =========================
        settings_map = {}

        settings_data = [
            ("INV", True, True, True),
            ("NCR", True, True, True),
            ("BILL", False, True, False),
            ("IN", True, False, False),
            ("OUT", True, False, False),
        ]

        for code, gen_inv, gen_acc, electronic in settings_data:
            setting, _ = DocumentSettings.objects.get_or_create(
                document_type=doc_type_map[code],
                defaults={
                    "initial_status": status_map["draft"],
                    "generate_inventory": gen_inv,
                    "generate_accounting": gen_acc,
                    "electronic": electronic,
                }
            )
            settings_map[code] = setting

        self.stdout.write(self.style.SUCCESS("✅ Configuraciones creadas"))

        # =========================
        # 4. SECUENCIAS
        # =========================
        sequence_data = [
            ("INV", "FAC-"),
            ("NCR", "NCR-"),
            ("BILL", "BILL-"),
            ("IN", "IN-"),
            ("OUT", "OUT-"),
        ]

        """
        for code, prefix in sequence_data:
            setting = settings_map[code]

            sequence, _ = DocumentSequence.objects.get_or_create(
                documentsettings=setting,
                defaults={
                    "prefix": prefix,
                    "last_number":0,
                    #"next_number": 1
                }
            )

            # asignar secuencia si no existe
            if not setting.sequence:
                setting.sequence = sequence
                setting.save()

        self.stdout.write(self.style.SUCCESS("✅ Secuencias creadas"))
        """
        # =========================
        # 5. WORKFLOWS
        # =========================
        workflows_data = [
            ("INV", "draft", "posted", "post"),
            ("INV", "posted", "cancelled", "cancel"),
            ("BILL", "draft", "posted", "post"),
        ]

        for doc_code, from_s, to_s, action in workflows_data:
            DocumentWorkflow.objects.get_or_create(
                document_type=doc_type_map[doc_code],
                from_status=status_map[from_s],
                to_status=status_map[to_s],
                defaults={"action": action}
            )

        self.stdout.write(self.style.SUCCESS("✅ Workflows creados"))

        self.stdout.write(self.style.SUCCESS("🎉 Carga inicial completada"))