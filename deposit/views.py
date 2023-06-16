from decimal import Decimal

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.conf import settings

from .models import Deposit, PendingTransaction
from .exchange_handler import buy_from_exchange
from .serializers import DepositSerializer

from cryptocurrency.models import Cryptocurrency
from wallet.models import Wallet

class ChargeWalletView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = request.data.get('amount')
        user = request.user

        if amount <= 0:
            return Response({'error': 'Amount must be greater than zero'}, status=status.HTTP_400_BAD_REQUEST)

        user.balance += amount
        user.save()
        Deposit(user=user, amount=amount).save()

        return Response({'message': f'Wallet charged with {amount} successfully'}, status=status.HTTP_200_OK)


class BuyCryptoView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        crypto_id = request.data.get('crypto_id')
        quantity = request.data.get('quantity')

        crypto = get_object_or_404(Cryptocurrency, id=crypto_id)
        amount = quantity * crypto.price_buy

        if user.balance < amount:
            return Response({'error': 'You must charge your personal wallet'}, status=status.HTTP_400_BAD_REQUEST)

        user.balance -= Decimal(amount)
        user.save()

        deposit = Deposit(user=request.user, crypto=crypto, amount=amount)
        deposit.save()
        wallet = Wallet.objects.get_or_create(user=user, crypto=crypto)[0]
            
        wallet.balance += Decimal(amount)
        wallet.quantity += quantity
        wallet.save()

        if amount >= settings.EXCHANGE_THRESHOLD:
            buy_from_exchange(crypto.symbol, amount)
            return Response(status=status.HTTP_201_CREATED)
        else:
            pending_transaction = PendingTransaction(user=user, crypto=crypto, amount=amount)
            pending_transaction.save()

            return Response(status=status.HTTP_201_CREATED)



class UserDepositView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        deposits = Deposit.objects.filter(user=user)
        serializer = DepositSerializer(deposits, many=True)
        return Response(serializer.data)