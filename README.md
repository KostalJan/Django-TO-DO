# My To-Do (Django + DRF + Templates)

A To-Do application with a REST API and server-rendered HTML views.  
`completed_at` is controlled centrally in `services.apply_status_effects` and used by both the API and the web action.

## Stack
- Python 3.12+
- Django 5
- Django REST Framework
- django-filter

## Local setup
```bash
python -m venv .venv
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
# Git Bash: source .venv/Scripts/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
