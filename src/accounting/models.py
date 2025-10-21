from common import models
from core.models import BaseModel


class Account(BaseModel):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=150)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    level = models.PositiveIntegerField(default=1)

class Project(BaseModel):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)

class CostCenter(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="cost_centers")
    name = models.CharField(max_length=150)
