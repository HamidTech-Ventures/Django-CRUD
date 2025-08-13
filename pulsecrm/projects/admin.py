from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "project_name", "client", "priority", "deadline", "budget")
    search_fields = ("project_name", "description")
    list_filter = ("priority", "deadline")