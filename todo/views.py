from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task
from .serializers import TaskSerializer
from .filters import TaskFilter


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by("-created_at")
    serializer_class = TaskSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TaskFilter
    # fulltext v titulku a popisu: ?search=nákup
    search_fields = ["title", "description"]
    # ?ordering=created_at nebo ?ordering=-created_at / -title / title
    ordering_fields = ["created_at", "title", "status", "category"]