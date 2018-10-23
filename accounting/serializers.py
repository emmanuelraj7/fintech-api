from rest_framework import serializers
from .models import Customers, Accounts, Transactions, Transfers




class WebhookSerializer(serializers.Serializer):
    """Serializer for checking recieved data format from scheme webhook"""

    type = serializers.CharField(max_length=16)
    card_id = serializers.CharField(max_length=16)
    transaction_id = serializers.CharField(max_length=16)
    merchant_name = serializers.CharField(max_length=255)
    merchant_country = serializers.CharField(max_length=4)
    merchant_city = serializers.CharField(max_length=128, required=False)
    merchant_mcc = serializers.IntegerField()
    billing_amount = serializers.DecimalField(max_digits=11, decimal_places=2)
    billing_currency = serializers.CharField(max_length=3)
    transaction_amount = serializers.DecimalField(max_digits=11, decimal_places=2)
    transaction_currency = serializers.CharField(max_length=3)
    settlement_amount = serializers.DecimalField(max_digits=11, decimal_places=2, required=False)
    settlement_currency = serializers.CharField(max_length=3, required=False)


class TransactionsSerializer(serializers.Serializer):
    """Serializer for checking format of data recieved through URL parameters"""

    cardholder = serializers.IntegerField()
    start_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    end_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')


class BalancesSerializer(serializers.Serializer):
    """Serializer for checking format of data recieved through URL parameters"""

    cardholder = serializers.IntegerField()
    type = serializers.CharField(max_length=9)
