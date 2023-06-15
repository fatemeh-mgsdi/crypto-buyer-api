from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Wallet
from .serializers import WalletSerializer



class UserWalletView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        wallets = Wallet.objects.filter(user=user)
        serializer = WalletSerializer(wallets, many=True)
        return Response(serializer.data)