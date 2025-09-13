from .models import *
from rest_framework import serializers

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"

class DevelopmentTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = DevelopmentTask
        fields = "__all__"

class DesignTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesignTask
        fields = "__all__"