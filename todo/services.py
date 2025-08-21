from django.utils import timezone
from .models import Task

def apply_status_effects(task: Task, new_status: str) -> Task:
    """
    Nastaví status a udržuje completed_at podle pravidel:
    - při 'done' vyplní completed_at, pokud ještě není
    - při jiném statusu vynuluje completed_at, pokud je vyplněné
    Nevolá .save() - ukládání je na volajícím.
    """
    old_status = task.status
    task.status = new_status

    if new_status == "done" and not task.completed_at:
        task.completed_at = timezone.now()
    elif new_status != "done" and task.completed_at:
        task.completed_at = None

    return task
