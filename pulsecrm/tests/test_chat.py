from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.models import User, UserRole
from clients.models import Client
from employees.models import Employee
from chat.models import Conversation, Message
from datetime import date


class ChatAPITests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(email="admin@example.com", password="adminpass", role=UserRole.ADMIN, is_staff=True)
        self.emp_user = User.objects.create_user(email="emp1@example.com", password="pass", role=UserRole.EMPLOYEE)
        self.employee = Employee.objects.create(
            user=self.emp_user,
            first_name="John",
            last_name="Doe",
            email="emp1@example.com",
            phone="",
            position="",
            department="",
            salary_per_month="0.00",
            start_date=date(2024,1,1),
            skills="",
            description="",
        )
        self.client_user = User.objects.create_user(email="client1@example.com", password="pass", role=UserRole.CLIENT)
        self.api = APIClient()

    def auth(self, user, password=None):
        resp = self.api.post(reverse('token_obtain_pair'), {"email": user.email, "password": password or ("adminpass" if user==self.admin else "pass")}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.api.credentials(HTTP_AUTHORIZATION=f"Bearer {resp.data['access']}")

    def test_admin_creates_conversation_with_employee(self):
        self.auth(self.admin)
        payload = {"participant_ids": [self.admin.id, self.emp_user.id]}
        resp = self.api.post("/api/chat/conversations/", payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        conv_id = resp.data["id"]
        # Admin sends message
        msg = {"conversation": conv_id, "sender": self.admin.id, "content": "Hello"}
        resp = self.api.post("/api/chat/messages/", msg, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Employee replies
        self.auth(self.emp_user)
        msg = {"conversation": conv_id, "sender": self.emp_user.id, "content": "Hi"}
        resp = self.api.post("/api/chat/messages/", msg, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_non_admin_cannot_create_conversation_without_admin(self):
        self.auth(self.emp_user)
        payload = {"participant_ids": [self.emp_user.id]}  # missing admin
        resp = self.api.post("/api/chat/conversations/", payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_mix_client_and_employee(self):
        self.auth(self.admin)
        payload = {"participant_ids": [self.admin.id, self.emp_user.id, self.client_user.id]}
        resp = self.api.post("/api/chat/conversations/", payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)