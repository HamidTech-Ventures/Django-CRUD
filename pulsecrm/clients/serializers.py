from rest_framework import serializers
from django.db import transaction
from users.models import User, UserRole
from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Client
        fields = [
            "id",
            "user_id",
            "contact_name",
            "company",
            "email",
            "phone",
            "industry",
            "website",
            "address",
            "description",
            "status",
            "joining_date",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "user_id"]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            instance = getattr(self, 'instance', None)
            if instance and instance.user and instance.user.email == value:
                return value
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        email = validated_data.get("email")
        contact_name = validated_data.get("contact_name")
        first_name = contact_name.split(" ")[0]
        last_name = " ".join(contact_name.split(" ")[1:]) if len(contact_name.split(" ")) > 1 else ""
        user = User.objects.create_user(email=email, password=User.objects.make_random_password(), first_name=first_name, last_name=last_name, role=UserRole.CLIENT, is_active=True)
        client = Client.objects.create(user=user, **validated_data)
        return client

    @transaction.atomic
    def update(self, instance: Client, validated_data):
        email = validated_data.get("email", instance.email)
        contact_name = validated_data.get("contact_name", instance.contact_name)
        user = instance.user
        if user.email != email:
            user.email = email
        parts = contact_name.split(" ")
        user.first_name = parts[0]
        user.last_name = " ".join(parts[1:]) if len(parts) > 1 else ""
        if user.role != UserRole.CLIENT:
            user.role = UserRole.CLIENT
        user.save()
        return super().update(instance, validated_data)