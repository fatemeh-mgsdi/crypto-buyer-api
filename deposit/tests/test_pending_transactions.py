from decimal import Decimal
from unittest.mock import patch

from django.test import TestCase

from deposit.models import PendingTransaction
from cryptocurrency.models import Cryptocurrency
from user.models import User
from deposit.tests.mock_data import user_data, crypto_data


class CheckPendingTransactionsSignalTestCase(TestCase):
    def setUp(self):
        self.crypto = Cryptocurrency.objects.create(**crypto_data)
        self.user = User.objects.create_user(**user_data)

    @patch("deposit.signals.buy_from_exchange")
    def test_check_pending_transactions_with_enough_amount(
        self, mock_buy_from_exchange
    ):
        mock_buy_from_exchange.assert_not_called()
        pending1 = PendingTransaction.objects.create(
            crypto=self.crypto, user=self.user, amount=Decimal("5.00")
        )
        pending2 = PendingTransaction.objects.create(
            crypto=self.crypto, user=self.user, amount=Decimal("6.00")
        )
        mock_buy_from_exchange.assert_called_once_with(
            self.crypto.symbol, Decimal("11.0000000000")
        )

        self.assertFalse(PendingTransaction.objects.filter(id=pending1.id).exists())
        self.assertFalse(PendingTransaction.objects.filter(id=pending2.id).exists())

    @patch("deposit.signals.buy_from_exchange")
    def test_check_pending_transactions_with_not_enough_amount(
        self, mock_buy_from_exchange
    ):
        mock_buy_from_exchange.assert_not_called()
        
        pending_transaction1 = PendingTransaction.objects.create(
            crypto=self.crypto, user=self.user, amount=Decimal("5.00")
        )
        pending_transaction2 = PendingTransaction.objects.create(
            crypto=self.crypto, user=self.user, amount=Decimal("4.00")
        )
        mock_buy_from_exchange.assert_not_called()

        self.assertTrue(
            PendingTransaction.objects.filter(id=pending_transaction1.id).exists()
        )
        self.assertTrue(
            PendingTransaction.objects.filter(id=pending_transaction2.id).exists()
        )
