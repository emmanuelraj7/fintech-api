from django.db import models
from django.utils import timezone


class Customers(models.Model):
    customer_name = models.CharField(max_length=30)
    card_id = models.IntegerField()
    total_balance = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)

    def __str__(self):
        return self.customer_name


class Accounts(models.Model):
    """Accounts Database Table"""

    id = models.BigAutoField(primary_key=True)
    customer_name = models.ForeignKey(Customers, on_delete=models.CASCADE)
    card_id = models.CharField(max_length=20, unique=True)
    currency = models.CharField(max_length=3)
    total_balance = models.DecimalField(max_digits=10, decimal_places=2)
    available_balance = models.DecimalField(max_digits=10, decimal_places=2)
    reserved_amount = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return self.card_id 
    


class Transactions(models.Model):
    """Represents the transactions DB table"""

    id = models.BigAutoField(primary_key=True)
    transaction_id = models.CharField(max_length=20, unique=True)
    type = models.CharField(max_length=16)
    card_id = models.ForeignKey(
        Accounts, on_delete=models.CASCADE, to_field='card_id')
    merchant_name = models.CharField(max_length=100)
    merchant_country = models.CharField(max_length=4)
    merchant_city = models.CharField(max_length=128, null=True, default=None)
    merchant_mcc = models.IntegerField()
    billing_amount = models.DecimalField(max_digits=10, decimal_places=2)
    billing_currency = models.CharField(max_length=3)
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_currency = models.CharField(max_length=3)
    settlement_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, default=None)
    settlement_currency = models.CharField(
        max_length=3, null=True, default=None)
    settled = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.transaction_id


class Transfers(models.Model):
    """Represents the transfers DB table"""

    CREDIT = 'CRT'
    DEBIT = 'DBT'
    TRANSFER_TYPE_CHOICES = (
        (CREDIT, 'Credit'),
        (DEBIT, 'Debit'),
    )

    id = models.BigAutoField(primary_key=True)
    transfer_type = models.CharField(max_length=3, choices=TRANSFER_TYPE_CHOICES, blank=True)  # Debit or credit.
    transaction = models.ForeignKey(Transactions, on_delete=models.CASCADE, to_field='transaction_id',
                                    null=True, default=None)  # Available if debit.
    account = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    total_balance = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.transfer_type




