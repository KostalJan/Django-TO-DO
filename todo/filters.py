import django_filters
from .models import Task

class TaskFilter(django_filters.FilterSet):
    # ?status=done
    status = django_filters.ChoiceFilter(choices=Task.STATUS_CHOICES)
    # ?category=prace  (case-insensitive)
    category = django_filters.CharFilter(field_name="category", lookup_expr="icontains")
    # ?created_after=2025-08-01&created_before=2025-08-31
    created_after = django_filters.IsoDateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_before = django_filters.IsoDateTimeFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = Task
        fields = ["status", "category", "created_after", "created_before"]