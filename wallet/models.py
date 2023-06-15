from django.db import models

from user.models import User
from cryptocurrency.models import Cryptocurrency

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    crypto = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE, null= True)
    quantity = models.IntegerField(default=0)
    balance = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def __str__(self):
        return f'{self.user.email} | {self.crypto.symbol} '

