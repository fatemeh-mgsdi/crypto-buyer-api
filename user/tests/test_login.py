from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from user.tests.mock_data import user_register_data, user_invalid_login_data, user_login_data
from user.models import User


class LoginTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse("login")
        self.user_register_data = user_register_data
        self.user = User.objects.create_user(**self.user_register_data)

    def test_valid_user_login(self):
        url = reverse("login")
        response = self.client.post(url, user_login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("token" in response.data)
        self.assertEqual(Token.objects.get(user=self.user).key, response.data["token"])

    def test_invalid_user_login(self):
        url = reverse("login")
        response = self.client.post(url, user_invalid_login_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
