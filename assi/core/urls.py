from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ProjectViewSet, DevelopmentTaskViewSet, DesignTaskViewSet


router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'dev-tasks', DevelopmentTaskViewSet)
router.register(r'design-tasks', DesignTaskViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
]
