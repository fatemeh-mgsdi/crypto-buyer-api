from django.db.models.signals import post_save
from django.db.models import Sum

from django.dispatch import receiver
from deposit.models import PendingTransaction

from deposit.exchange_handler import buy_from_exchange

@receiver(post_save, sender=PendingTransaction)
def check_pending_transactions(sender, instance, created, **kwargs):
    total_amounts = PendingTransaction.objects.select_related('crypto').values('crypto__symbol').annotate(total=Sum('amount'))

    for total_amount in total_amounts:
        if total_amount['total'] >= 10:
            buy_from_exchange(total_amount['crypto__symbol'], total_amount['total'])
            PendingTransaction.objects.filter(crypto__symbol=total_amount['crypto__symbol']).delete()