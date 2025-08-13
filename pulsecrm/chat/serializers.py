from rest_framework import serializers
from django.db import transaction
from users.models import User, UserRole
from .models import Conversation, Message


class ConversationSerializer(serializers.ModelSerializer):
    participant_ids = serializers.PrimaryKeyRelatedField(source='participants', queryset=User.objects.all(), many=True)

    class Meta:
        model = Conversation
        fields = ["id", "participant_ids", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate(self, attrs):
        participants = list(attrs.get('participants', []))
        # enforce that Admin must be participant
        role_set = set(p.role for p in participants)
        if UserRole.ADMIN not in role_set:
            raise serializers.ValidationError("An Admin must be a participant in the conversation.")
        # Must include exactly one non-admin participant for 1:1 admin chat
        non_admins = [p for p in participants if p.role != UserRole.ADMIN]
        if len(non_admins) != 1:
            raise serializers.ValidationError("Conversation must include exactly one non-admin participant.")
        # ensure not mixing roles since it's exactly one
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        participants = validated_data.pop('participants', [])
        conversation = Conversation.objects.create(**validated_data)
        conversation.participants.set(participants)
        return conversation

    @transaction.atomic
    def update(self, instance, validated_data):
        participants = validated_data.pop('participants', None)
        conversation = super().update(instance, validated_data)
        if participants is not None:
            conversation.participants.set(participants)
        return conversation


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    conversation = serializers.PrimaryKeyRelatedField(queryset=Conversation.objects.all())

    class Meta:
        model = Message
        fields = ["id", "conversation", "sender", "content", "is_read", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate(self, attrs):
        user = self.context["request"].user
        sender = attrs.get("sender")
        conversation = attrs.get("conversation")
        if sender != user:
            raise serializers.ValidationError("Sender must be the authenticated user.")
        if not conversation.participants.filter(id=sender.id).exists():
            raise serializers.ValidationError("Sender must be a participant in the conversation.")
        # employees/clients can only message Admin within the conversation
        participant_roles = set(conversation.participants.values_list("role", flat=True))
        if sender.role in {UserRole.EMPLOYEE, UserRole.CLIENT} and UserRole.ADMIN not in participant_roles:
            raise serializers.ValidationError("Non-admin users can only message Admin.")
        return attrs