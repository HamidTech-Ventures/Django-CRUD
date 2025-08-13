from django.contrib import admin
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "contact_name", "email", "status", "joining_date")
    search_fields = ("company", "contact_name", "email", "industry")
    list_filter = ("status", "joining_date")