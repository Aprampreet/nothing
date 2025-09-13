from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["status", "start_date", "end_date"]
    search_fields = ["title", "description"]
    ordering_fields = ["start_date", "end_date", "created_at"]


class DevelopmentTaskViewSet(viewsets.ModelViewSet):
    queryset = DevelopmentTask.objects.all()
    serializer_class = DevelopmentTaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["status", "priority", "due_date"]
    search_fields = ["title", "programming_language"]
    ordering_fields = ["due_date", "priority"]

class DesignTaskViewSet(viewsets.ModelViewSet):
    queryset = DesignTask.objects.all()
    serializer_class = DesignTaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["status", "priority", "due_date"]
    search_fields = ["title", "design_tool"]
    ordering_fields = ["due_date", "priority"]
