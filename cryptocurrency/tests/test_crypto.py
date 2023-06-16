from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from cryptocurrency.models import Cryptocurrency
from cryptocurrency.serializers import CryptocurrencySerializer
from user.models import User
from cryptocurrency.tests.mock_data import *


class CryptoViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.superuser = User.objects.create_superuser(**admin_data)
        self.token = Token.objects.create(user=self.superuser)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        self.crypto1 = Cryptocurrency.objects.create(**crypto1_data)
        self.crypto2 = Cryptocurrency.objects.create(**crypto2_data)

    def test_get_crypto_list(self):
        url = reverse("cryptocurrency-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["name"], self.crypto1.name)
        self.assertEqual(response.data[1]["symbol"], self.crypto2.symbol)

    def test_get_crypto_detail(self):
        url = reverse("cryptocurrency-detail", args=[self.crypto1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = CryptocurrencySerializer(self.crypto1)
        self.assertEqual(response.data, serializer.data)

    def test_create_crypto(self):
        url = reverse("cryptocurrency-list")

        response = self.client.post(url, create_crypto_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cryptocurrency.objects.count(), 3)
        self.assertEqual(
            Cryptocurrency.objects.get(symbol="LTC").name, create_crypto_data["name"]
        )

    def test_update_crypto(self):
        url = reverse("cryptocurrency-detail", args=[self.crypto1.id])
        response = self.client.put(url, update_crypto_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Cryptocurrency.objects.get(id=self.crypto1.id).price_buy,
            Decimal(update_crypto_data["price_buy"]),
        )

        self.assertEqual(
            Cryptocurrency.objects.get(id=self.crypto1.id).price_sell,
            Decimal(update_crypto_data["price_sell"]),
        )

    def test_delete_crypto(self):
        url = reverse("cryptocurrency-detail", args=[self.crypto1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Cryptocurrency.objects.count(), 1)

    def test_change_past24(self):
        url = reverse("cryptocurrency-change-past24", args=[self.crypto1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Decimal(response.data["past24"]), 1000)


class CreateCryptoByNormalUserTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(**regular_user_data)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_create_crypto(self):
        url = reverse("cryptocurrency-list")
        response = self.client.post(url, create_crypto_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
