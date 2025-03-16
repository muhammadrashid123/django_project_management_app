# Django Project Management App

## Features
- User Authentication
- Project CRUD with Role-Based Access Control (RBAC)
- Comments on projects (Owner/Editor only)
- Admin Interface
- Swagger API Documentation

## Setup Instructions
```bash
git@github.com:muhammadrashid123/django_project_management_app.git
cd django_project_management_app
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## API Docs
Visit /swagger/ for interactive API testing.
http://127.0.0.1:8000/swagger/

## Roles
- Owner
- Editor
- Reader

