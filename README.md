# Django Project Management App

## Features
- User Authentication
- Project CRUD with Role-Based Access Control (RBAC)
- Comments on projects (Owner/Editor only)
- Admin Interface
- Swagger API Documentation

## Setup Instructions
```bash
git clone https://github.com/your-repo/project-management.git
cd project-management
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## API Docs
Visit /swagger/ for interactive API testing.

## Roles
- Owner
- Editor
- Reader

