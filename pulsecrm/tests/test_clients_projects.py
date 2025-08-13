from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.models import User, UserRole
from clients.models import Client
from employees.models import Employee
from projects.models import Project, ProjectPriority
from datetime import date


class ClientsProjectsAPITests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(email="admin@example.com", password="adminpass", role=UserRole.ADMIN, is_staff=True)
        self.emp_user = User.objects.create_user(email="emp@example.com", password="pass", role=UserRole.EMPLOYEE)
        self.employee = Employee.objects.create(
            user=self.emp_user,
            first_name="Jane",
            last_name="Doe",
            email="emp@example.com",
            phone="",
            position="Dev",
            department="Eng",
            salary_per_month="6000.00",
            start_date=date(2024,1,10),
            skills="",
            description="",
        )
        self.client = APIClient()

    def auth(self, user):
        resp = self.client.post(reverse('token_obtain_pair'), {"email": user.email, "password": "adminpass" if user==self.admin else "pass"}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {resp.data['access']}")

    def test_admin_crud_client(self):
        self.auth(self.admin)
        payload = {
            "contact_name": "Bob",
            "company": "Acme",
            "email": "bob@acme.com",
            "phone": "",
            "industry": "Tech",
            "website": "https://acme.com",
            "address": "",
            "description": "",
            "status": "Active",
            "joining_date": "2024-01-15"
        }
        resp = self.client.post("/api/clients/", payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        client_id = resp.data["id"]
        resp = self.client.get(f"/api/clients/{client_id}/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        resp = self.client.patch(f"/api/clients/{client_id}/", {"status":"Complete"}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        resp = self.client.delete(f"/api/clients/{client_id}/")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_non_admin_cannot_access_clients(self):
        self.auth(self.emp_user)
        resp = self.client.get("/api/clients/")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_create_project_with_dropdowns(self):
        self.auth(self.admin)
        client_user = User.objects.create_user(email="carl@widgets.com", password="pass", role=UserRole.CLIENT)
        client = Client.objects.create(
            user=client_user,
            contact_name="Carl",
            company="Widgets Inc",
            email="carl@widgets.com",
            phone="",
            industry="Tech",
            website="https://widgets.com",
            address="",
            description="",
            status="Active",
            joining_date=date(2024,1,20),
        )
        payload = {
            "project_name": "Website Redesign",
            "client": client.id,
            "description": "",
            "budget": "10000.00",
            "priority": "High",
            "deadline": "2024-12-31",
            "team": [self.employee.id]
        }
        resp = self.client.post("/api/projects/", payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        proj_id = resp.data["id"]
        resp = self.client.get(f"/api/projects/{proj_id}/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["client"], client.id)
        self.assertEqual(resp.data["team"], [self.employee.id])

    def test_non_admin_cannot_access_projects(self):
        self.auth(self.emp_user)
        resp = self.client.get("/api/projects/")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)