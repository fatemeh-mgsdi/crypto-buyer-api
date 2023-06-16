from django.db.models.signals import pre_delete
from django.dispatch import receiver

from cryptocurrency.models import Cryptocurrency
from wallet.models import Wallet


@receiver(pre_delete, sender=Cryptocurrency)
def handle_crypto_delete(sender, instance, **kwargs):
    wallets = Wallet.objects.filter(crypto=instance)

    for wallet in wallets:
        wallet.user.balance += wallet.balance
        wallet.user.save()
