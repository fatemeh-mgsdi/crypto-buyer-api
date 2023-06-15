from django.db import models
from user.models import User
from cryptocurrency.models import Cryptocurrency


class Deposit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE, null= True)
    amount = models.DecimalField(max_digits=20, decimal_places=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Deposit {self.amount} {self.crypto.symbol} into {self.wallet.user.email}\'s wallet'


class PendingTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Pending transaction {self.amount} {self.crypto.symbol} for {self.user.email}'
