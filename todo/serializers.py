from rest_framework import serializers
from .models import Task
from django.utils import timezone


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "description", "status", "category", "created_at", "completed_at"]
        read_only_fields = ["created_at", "completed_at"]

    def update(self, instance, validated_data):
        #změna nastavení completed_at v závsislost na status
        old_status = instance.status
        new_status = validated_data.get("status", old_status)

        if new_status == "done" and (instance.completed_at is None):
            validated_data["completed_at"] = timezone.now()
        elif new_status != "done" and (instance.completed_at is not None):
            validated_data["completed_at"] = None

        return super().update(instance, validated_data)

    def create(self, validated_data):
        # pokud se vytváří task rovnou se statusem "done", nastaví se completed_at
        if validated_data.get("status") == "done" and not validated_data.get("completed_at"):
            validated_data["completed_at"] = timezone.now()
        return super().create(validated_data)