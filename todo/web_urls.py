from django.urls import path
from . import web_views

urlpatterns = [
    path("tasks/", web_views.tasks_list, name="tasks_list"),
    path("tasks/new/", web_views.task_create, name="task_create"),
    path("tasks/<int:pk>/done/", web_views.task_mark_done, name="task_mark_done"),
]
