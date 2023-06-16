from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from user.models import User
from deposit.tests.mock_data import user_data


class ChargeWalletViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(**user_data)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_charge_wallet_with_valid_amount(self):
        url = reverse("charge_wallet")
        data = {"amount": 100}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.balance, Decimal("100.00"))

    def test_charge_wallet_with_zero_amount(self):
        url = reverse("charge_wallet")
        data = {"amount": 0}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Amount must be greater than zero")

    def test_charge_wallet_with_negative_amount(self):
        url = reverse("charge_wallet")
        data = {"amount": -39}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Amount must be greater than zero")
