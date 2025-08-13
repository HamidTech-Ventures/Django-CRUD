from rest_framework import serializers
from django.db import transaction
from users.models import User, UserRole
from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Employee
        fields = [
            "id",
            "user_id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "position",
            "department",
            "salary_per_month",
            "start_date",
            "skills",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "user_id"]

    def validate_email(self, value):
        # Ensure unique across Users as well
        if User.objects.filter(email=value).exists():
            # allow if it's the same as existing user linked to this instance
            instance = getattr(self, 'instance', None)
            if instance and instance.user and instance.user.email == value:
                return value
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        email = validated_data.get("email")
        first_name = validated_data.get("first_name")
        last_name = validated_data.get("last_name")
        # Auto-create a user with random password
        user = User.objects.create_user(email=email, password=User.objects.make_random_password(), first_name=first_name, last_name=last_name, role=UserRole.EMPLOYEE, is_active=True)
        employee = Employee.objects.create(user=user, **validated_data)
        return employee

    @transaction.atomic
    def update(self, instance: Employee, validated_data):
        email = validated_data.get("email", instance.email)
        first_name = validated_data.get("first_name", instance.first_name)
        last_name = validated_data.get("last_name", instance.last_name)
        # keep user in sync
        user = instance.user
        if user.email != email:
            user.email = email
        user.first_name = first_name
        user.last_name = last_name
        if user.role != UserRole.EMPLOYEE:
            user.role = UserRole.EMPLOYEE
        user.save()
        return super().update(instance, validated_data)