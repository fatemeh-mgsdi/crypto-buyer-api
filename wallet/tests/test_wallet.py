from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from user.models import User
from cryptocurrency.models import Cryptocurrency
from wallet.models import Wallet
from wallet.tests.mock_data import user_data, crypto_data


class WalletViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(**user_data)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        
        self.crypto = Cryptocurrency.objects.create(**crypto_data)

    def test_wallet(self):
        url = reverse("charge_wallet")
        data = {"amount": 20}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        url = reverse("buy_crypto")
        data = {"crypto_id": self.crypto.id, "quantity": 4}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        wallet = Wallet.objects.get()
        self.assertEqual(wallet.user, self.user)
        self.assertEqual(wallet.crypto, self.crypto)
        self.assertEqual(wallet.balance, Decimal("16.00"))
        self.assertEqual(wallet.quantity, 4)
