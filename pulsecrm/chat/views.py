from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from users.models import UserRole
from users.permissions import IsConversationParticipantOrAdmin
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsConversationParticipantOrAdmin]

    def get_queryset(self):
        user = self.request.user
        base = Conversation.objects.prefetch_related("participants")
        if user.role == UserRole.ADMIN:
            return base
        return base.filter(participants=user)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsConversationParticipantOrAdmin]

    def get_queryset(self):
        user = self.request.user
        base = Message.objects.select_related("conversation").select_related("sender").filter(
            Q(conversation__participants=user) | Q(conversation__participants__role=UserRole.ADMIN)
        ).distinct()
        if user.role == UserRole.ADMIN:
            return base
        return base.filter(conversation__participants=user)

    def perform_create(self, serializer):
        serializer.save()