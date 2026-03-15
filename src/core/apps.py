from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.core.management import call_command


def load_initial_data(sender, **kwargs):
    """
    Carga los datos iniciales automáticamente después de aplicar las migraciones.
    Solo se ejecuta una vez, cuando el app 'core' termina sus migraciones.
    """
    try:
        print("🚀 Ejecutando carga inicial de datos base...")
        call_command("load_initial_data")
    except Exception as e:
        print(f"⚠️ Error cargando datos iniciales: {e}")


class CoreConfig(AppConfig):
    name = "core"

    def ready(self):
        post_migrate.connect(load_initial_data, sender=self)
"""
from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
"""