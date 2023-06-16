from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from user.tests.mock_data import user_register_data
from user.models import User


class RegisterTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse("register")
        self.user_register_data = user_register_data

    def test_valid_user_register(self):
        response = self.client.post(self.register_url, self.user_register_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, user_register_data["email"])
        self.assertTrue(
            User.objects.get().check_password(user_register_data["password"])
        )
    
    def test_duplicate_user_register(self):
        response = self.client.post(self.register_url, self.user_register_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(self.register_url, self.user_register_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

