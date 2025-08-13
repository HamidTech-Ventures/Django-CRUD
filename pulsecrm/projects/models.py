from django.db import models
from django.core.validators import MinValueValidator
from clients.models import Client
from employees.models import Employee


class ProjectPriority(models.TextChoices):
    LOW = "Low", "Low"
    MEDIUM = "Medium", "Medium"
    HIGH = "High", "High"


class Project(models.Model):
    project_name = models.CharField(max_length=200)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="projects")
    description = models.TextField(blank=True)
    budget = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0)])
    priority = models.CharField(max_length=10, choices=ProjectPriority.choices, default=ProjectPriority.MEDIUM)
    deadline = models.DateField()
    team = models.ManyToManyField(Employee, related_name="projects", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["priority"]),
            models.Index(fields=["deadline"]),
        ]

    def __str__(self) -> str:
        return self.project_name