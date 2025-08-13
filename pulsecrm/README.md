Pulse CRM - Backend (Django + DRF + PostgreSQL)

Tech stack
- Django 5, DRF, PostgreSQL, JWT (SimpleJWT), django-environ

Setup
1) Create and activate a virtualenv, then install dependencies:
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

2) Configure environment variables:
   cp .env.example .env
   # Edit .env to match your PostgreSQL settings

3) Run migrations and create a superuser (Admin):
   python manage.py migrate
   python manage.py createsuperuser

4) Run the server:
   python manage.py runserver 0.0.0.0:8000

Auth
- Obtain JWT: POST /api/auth/token/ {"email":"admin@example.com","password":"..."}
- Refresh JWT: POST /api/auth/token/refresh/ {"refresh":"..."}

Apps & Endpoints (all under /api/)
- Employees: /employees/
- Clients: /clients/
- Projects: /projects/
- Chat: /chat/conversations/, /chat/messages/

Notes
- Only Admin users can perform CRUD on Employees, Clients, and Projects.
- Chat: Admin can message Employees and Clients. Employees/Clients can message Admin only.
- Filtering, searching, ordering supported via DRF filters.