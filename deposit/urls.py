from django.urls import path

from .views import ChargeWalletView, BuyCryptoView, UserDepositView


urlpatterns = [
    path('deposit/charge-wallet/', ChargeWalletView.as_view(), name='charge_wallet'),
    path('deposit/buy-crypto/', BuyCryptoView.as_view(), name='buy_crypto'),
    path('deposit/', UserDepositView.as_view(), name='user_deposits'),
]