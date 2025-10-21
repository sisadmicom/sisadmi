#people/models.py
from django.db import models
from core.models import BaseModel

class Country(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    def __str__(self):
        return self.name


class Province(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="provinces")
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Canton(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name="cantons")
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Parish(models.Model):
    canton = models.ForeignKey(Canton, on_delete=models.CASCADE, related_name="parishes")
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Gender(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=25)
    def __str__(self):
        return f"{self.name} {self.symbol}" if self.name else self.name


class Person(BaseModel):
    NATURAL = "N"
    LEGAL = "J"
    TYPE_CHOICES = [
        (NATURAL, "Natural"),
        (LEGAL, "Jurídica"),
    ]

    identification = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, blank=True)
    company_name = models.CharField(max_length=300, blank=True)
    person_type = models.CharField(max_length=1, choices=TYPE_CHOICES, default=NATURAL)
    email = models.EmailField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True)
    parish = models.ForeignKey(Parish, on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    # Auditoría
    created_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_people'  # 👈 evita el conflicto con user.person
    )

    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"

    def __str__(self):
        return f"{self.name} {self.last_name}".strip()


class Client(BaseModel):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, related_name="client_profile")
    client_type = models.CharField(max_length=50, blank=True, null=True)
    zone = models.CharField(max_length=100, blank=True, null=True)
    credit_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.person)


class Supplier(BaseModel):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, related_name="supplier_profile")
    contact_person = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return str(self.person)


class Employee(BaseModel):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, related_name="employee_profile")
    position = models.CharField(max_length=100)
    profession = models.CharField(max_length=100, blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hire_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.person)
