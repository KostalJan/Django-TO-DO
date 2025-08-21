from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Task
from .forms import TaskForm
from .services import apply_status_effects


def tasks_list(request):
    """
    HTML seznam úkolů se základními filtry a stránkováním.
    Filtry: ?status=, ?category= (icontains), ?search= (v title/description)
    """
    qs = Task.objects.all().order_by("-created_at")

    status_v = request.GET.get("status") or ""
    category_v = request.GET.get("category") or ""
    search_v = request.GET.get("search") or ""

    if status_v:
        qs = qs.filter(status=status_v)
    if category_v:
        qs = qs.filter(category__icontains=category_v)
    if search_v:
        qs = qs.filter(Q(title__icontains=search_v) | Q(description__icontains=search_v))

    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "page_obj": page_obj,
        "filters": {"status": status_v, "category": category_v, "search": search_v},
    }
    return render(request, "todo/tasks_list.html", context)


def task_create(request):
    """
    Vytvoření nového úkolu přes HTML formulář.
    """
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("tasks_list")
    else:
        form = TaskForm()
    return render(request, "todo/task_form.html", {"form": form})


def task_mark_done(request, pk: int):
    """
    Označení úkolu za hotový (POST).
    """
    if request.method != "POST":
        return redirect("tasks_list")

    task = get_object_or_404(Task, pk=pk)
    apply_status_effects(task, "done")
    task.save(update_fields=["status", "completed_at"])
    return redirect("tasks_list")
