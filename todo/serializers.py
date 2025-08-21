from rest_framework import serializers
from .models import Task
from django.utils import timezone
from .services import apply_status_effects


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "description", "status", "category", "created_at", "completed_at"]
        read_only_fields = ["created_at", "completed_at"]

    def update(self, instance, validated_data):
        #při update vyjmeme z Tasku status a nastavíme ho dle service funkce
        new_status = validated_data.pop("status", instance.status)
        apply_status_effects(instance, new_status)

        # ostatní pole se klasicky nastaví
        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()
        return instance

    def create(self, validated_data):
        # při vytváření se také status nastavuje dle service funkce
        new_status = validated_data.pop("status", "todo")
        task = Task(**validated_data)
        apply_status_effects(task, new_status)
        task.save()
        return task