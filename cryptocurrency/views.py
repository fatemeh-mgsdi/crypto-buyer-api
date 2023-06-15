from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

from .serializers import CryptocurrencySerializer
from .models import Cryptocurrency
from cryptocurrency.permissions import IsSuperUser

class CryptoViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    queryset = Cryptocurrency.objects.all()
    serializer_class = CryptocurrencySerializer
    permission_classes = [IsSuperUser]

    @action(detail=True, methods=['get'])
    def change_past24(self, request, pk=None):
        crypto = self.get_object()
        past24 = crypto.price_buy - crypto.price_sell
        crypto.past24 = past24
        crypto.save()
        serializer = CryptocurrencySerializer(crypto)
        return Response(serializer.data)