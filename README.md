Project & Task Management System

A streamlined Project & Task Management application built with Django, Django REST Framework, Celery, and Django Admin.
Designed to demonstrate professional Django practices, including signals, task automation, inline admin editing, and REST APIs.

Features

Projects & Tasks

Projects with multiple Development & Design tasks.

Task priority, status, and due dates.

Inline editing of tasks in Django Admin.

REST API

CRUD endpoints for Projects, DevelopmentTask, and DesignTask.

Filtering, searching, and ordering.

Signals

Email notifications on task creation.

Cascade notifications when a project is deleted.

Celery Integration

Automatic marking of overdue tasks via Celery Beat.

Email notifications for overdue tasks.

Admin

Filters, search, readonly fields, and bulk actions.

Testing

Unit tests for models, signals, APIs, and Celery tasks.

Tech Stack

Python 3.11+

Django 5.x

Django REST Framework

Celery + Redis

PostgreSQL (or SQLite for local dev)

Docker (optional)

Redis (for Celery broker & backend)

Setup Instructions
1. Clone the Repository
git clone https://github.com/Aprampreet/nothing.git
cd project-management

2. Create Virtual Environment
python -m venv env
source env/bin/activate   

3. Install Dependencies
pip install -r requirements.txt

requirements.txt should include:

Django>=5.0
djangorestframework
django-filter
celery
redis


4. Apply Migrations
python manage.py makemigrations
python manage.py migrate

5. Create Superuser
python manage.py createsuperuser

6. Run the Development Server
python manage.py runserver


Access admin at: http://127.0.0.1:8000/admin/
