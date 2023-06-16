from django.db import models


class Cryptocurrency(models.Model):
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=255, unique=True)
    price_buy = models.DecimalField(max_digits=20, decimal_places=10)
    price_sell = models.DecimalField(max_digits=20, decimal_places=10)
    last_update = models.DateTimeField(auto_now=True)
    past24 = models.DecimalField(max_digits=20, decimal_places=10, default=0)

    def __str__(self):
        return f"{self.name} | {self.symbol}"
