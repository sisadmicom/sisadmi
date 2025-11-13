from django.apps import AppConfig
#from django.db.models.signals import post_migrate
"""
def load_initial_data(sender, **kwargs):
    from django.apps import apps
    if apps.is_installed("core"):
        from django.core.management import call_command
        call_command("load_initial_data")
"""
class CompaniesConfig(AppConfig):
    name = "companies"
"""
    def ready(self):
        # 🔁 Conectamos al post_migrate para ejecutar los datos iniciales
        post_migrate.connect(load_initial_data, sender=self)
"""