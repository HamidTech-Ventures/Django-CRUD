from django.db import models
from django.conf import settings


class ClientStatus(models.TextChoices):
    ACTIVE = "Active", "Active"
    COMPLETE = "Complete", "Complete"
    PROSPECTS = "Prospects", "Prospects"


class Client(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="client_profile")
    contact_name = models.CharField(max_length=150)
    company = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50, blank=True)
    industry = models.CharField(max_length=150, blank=True)
    website = models.URLField(blank=True)
    address = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=ClientStatus.choices, default=ClientStatus.PROSPECTS)
    joining_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.company} ({self.contact_name})"