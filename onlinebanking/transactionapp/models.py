from enum import unique
from django.db import models
from django.forms import CharField
from onlinebanking.staffapp.models import profile
from django.contrib.auth.models import User
from django.utils import timezone

account_type = [
    ("Savings", "Savings"),
    ("Current", "Current"),
    ("Fixed Deposit", "Fixed Deposit"),
]

# transaction_type = [
#     ("Deposit"), ("Deposit"),
#     ("Withdrawal"), ("Withdrawal"),
# ]

# Create your models here.
class Account_table(models.Model):
    account_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_balance = models.BigIntegerField(unique=False, null=True)
    account_type = models.CharField(choices=account_type, unique=False, max_length=20, null=True)
    account_number = models.CharField(unique=True, max_length=10, default=10101010)
    future_transaction = models.DateTimeField(null=True, unique=False, max_length=20)
    account_pin = models.IntegerField(unique=False, default=0000)

class Transaction_table(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account_table, on_delete=models.CASCADE)
    transaction_type = models.CharField(unique=False, max_length=20)
    transaction_date = models.DateTimeField(default=timezone.now)
    account_number = models.CharField(unique=False, max_length=10, null=True)
    sender_account = models.CharField(unique=False, max_length=10, null=True)
    transaction_amount = models.BigIntegerField(unique=False, null=True)
    recipient_number = models.CharField(unique=False, max_length=10, null=True)
    recipient_bank = models.CharField(unique=False, max_length=20, null=True)

class Future_transaction_table(models.Model):
    future_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    owner_account =  models.CharField(unique=False, max_length=10)
    recipient_account = models.CharField(unique=False, max_length=10)
    recipient_bank = models.CharField(unique=False, max_length=20, null=True)
    transaction_type = models.CharField(unique=False, max_length=20)
    transaction_amount = models.BigIntegerField(unique=False, null=True)
    future_date = models.DateField()
    future_time = models.TimeField()
