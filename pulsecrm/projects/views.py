from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from users.permissions import IsAdminRole
from .models import Project
from .serializers import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.select_related("client").prefetch_related("team").all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["priority", "deadline", "client"]
    search_fields = ["project_name", "description", "client__company"]
    ordering_fields = ["deadline", "budget", "project_name", "created_at"]