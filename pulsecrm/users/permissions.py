from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import UserRole


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == UserRole.ADMIN)


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsConversationParticipantOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.role == UserRole.ADMIN:
            return True
        # obj can be Conversation or Message
        if hasattr(obj, "participants"):
            return obj.participants.filter(id=user.id).exists()
        if hasattr(obj, "conversation"):
            return obj.conversation.participants.filter(id=user.id).exists()
        return False