# companies/models.py
from django.db import models
from core.models import BaseModel

class Company(BaseModel):
    """
    Representa una empresa dentro del sistema.
    Multiempresa: cada registro puede pertenecer a una compañía.
    """

    name = models.CharField(max_length=200, unique=True)
    trade_name = models.CharField(max_length=200, blank=True, null=True)
    ruc = models.CharField(max_length=20, unique=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Branch(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="branches")
    name = models.CharField(max_length=150)
    address = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name