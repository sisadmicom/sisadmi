from django.contrib import admin
from core.models import BaseModel, TimeStampedModel  # solo si los necesitas como referencia

# No registres modelos abstractos
# Si tienes modelos concretos, regístralos así:
# from companies.models import Company
# admin.site.register(Company)
