from decimal import Decimal

from django.db import models

from user.models import User
from cryptocurrency.models import Cryptocurrency

class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE, null= True)
    quantity = models.IntegerField(default=0)
    balance = models.DecimalField(max_digits=20, decimal_places=10, default=Decimal('0.0'))

    class Meta:
        unique_together = ('user', 'crypto')

    def __str__(self):
        return f'{self.user.email} | {self.crypto.symbol} '

