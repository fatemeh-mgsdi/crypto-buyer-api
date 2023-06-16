from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from user.models import User
from cryptocurrency.models import Cryptocurrency
from deposit.models import Deposit
from deposit.tests.mock_data import user_data, crypto_data


class UserDepositViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(**user_data)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        self.crypto = Cryptocurrency.objects.create(**crypto_data)

    def test_get_user_deposits(self):
        url = reverse("charge_wallet")
        data = {"amount": 15}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()

        url = reverse("buy_crypto")
        data = {"crypto_id": self.crypto.id, "quantity": 2}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Deposit.objects.count(), 2)
