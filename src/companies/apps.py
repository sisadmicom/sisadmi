from django.apps import AppConfig
from django.db.models.signals import post_migrate

def create_default_company(sender, **kwargs):
    from companies.models import Company, Branch

    if not Company.objects.exists():
        company = Company.objects.create(
            name="Sisadmi.com",
            trade_name="Matriz",
            ruc="9999999999999",
            address="NA",
            phone="0000000",
            email="sis@dmi.com",
            is_active=True
        )
        Branch.objects.create(
            company=company,
            name="Sucursal Principal",
            address="Dirección principal"
        )
        print("✅ Se creó la empresa y sucursal por defecto.")


class CompaniesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'companies'

    def ready(self):
        post_migrate.connect(create_default_company, sender=self)
        # Conectamos también las señales (en signals.py)
        from . import signals  # noqa