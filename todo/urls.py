from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet

router = DefaultRouter(trailing_slash='/?')
router.register(r"tasks", TaskViewSet, "task")

urlpatterns = [
    path("", include(router.urls)),
]