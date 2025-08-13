from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.models import User, UserRole
from employees.models import Employee
from datetime import date


class EmployeesAPITests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(email="admin@example.com", password="adminpass", role=UserRole.ADMIN, is_staff=True)
        self.emp_user = User.objects.create_user(email="emp1@example.com", password="pass", role=UserRole.EMPLOYEE)
        self.employee = Employee.objects.create(
            user=self.emp_user,
            first_name="John",
            last_name="Doe",
            email="emp1@example.com",
            phone="123",
            position="Dev",
            department="Engineering",
            salary_per_month="5000.00",
            start_date=date(2024,1,1),
            skills="Python",
            description="",
        )
        self.client = APIClient()

    def auth(self, user):
        resp = self.client.post(reverse('token_obtain_pair'), {"email": user.email, "password": "adminpass" if user==self.admin else "pass"}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {resp.data['access']}")

    def test_admin_can_list_employees(self):
        self.auth(self.admin)
        resp = self.client.get("/api/employees/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(resp.data), 1)

    def test_non_admin_cannot_list_employees(self):
        self.auth(self.emp_user)
        resp = self.client.get("/api/employees/")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_employee(self):
        self.auth(self.admin)
        payload = {
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice@example.com",
            "phone": "",
            "position": "PM",
            "department": "Product",
            "salary_per_month": "7000.00",
            "start_date": "2024-02-01",
            "skills": "Management",
            "description": "",
        }
        resp = self.client.post("/api/employees/", payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="alice@example.com").exists())

    def test_admin_can_update_employee(self):
        self.auth(self.admin)
        resp = self.client.patch(f"/api/employees/{self.employee.id}/", {"position": "Senior Dev"}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.position, "Senior Dev")

    def test_admin_can_delete_employee(self):
        self.auth(self.admin)
        resp = self.client.delete(f"/api/employees/{self.employee.id}/")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)