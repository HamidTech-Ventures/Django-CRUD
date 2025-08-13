from rest_framework import serializers
from django.db import transaction
from clients.models import Client
from employees.models import Employee
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all())
    team = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), many=True, required=False)

    class Meta:
        model = Project
        fields = [
            "id",
            "project_name",
            "client",
            "description",
            "budget",
            "priority",
            "deadline",
            "team",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    @transaction.atomic
    def create(self, validated_data):
        team_ids = validated_data.pop("team", [])
        project = Project.objects.create(**validated_data)
        if team_ids:
            project.team.set(team_ids)
        return project

    @transaction.atomic
    def update(self, instance, validated_data):
        team_ids = validated_data.pop("team", None)
        project = super().update(instance, validated_data)
        if team_ids is not None:
            project.team.set(team_ids)
        return project