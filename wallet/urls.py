from django.urls import path

from .views import UserWalletView


urlpatterns = [
    path('wallet/', UserWalletView.as_view(), name='user_wallets'),
]