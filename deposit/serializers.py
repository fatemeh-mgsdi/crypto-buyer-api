from rest_framework import serializers
from .models import Deposit

class DepositSerializer(serializers.ModelSerializer):
    crypto_symbol = serializers.ReadOnlyField(source='crypto.symbol')

    class Meta:
        model = Deposit
        fields = '__all__'