from django.db import models
from django.contrib.auth.models import User
import random


# ==========================
# Account Model
# ==========================
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=12, unique=True, blank=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.account_number:
            while True:
                number = str(random.randint(100000000000, 999999999999))
                if not Account.objects.filter(account_number=number).exists():
                    self.account_number = number
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.account_number}"


# ==========================
# Transaction Model
# ==========================
class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('Deposit', 'Deposit'),
        ('Withdraw', 'Withdraw'),
        ('Transfer Sent', 'Transfer Sent'),
        ('Transfer Received', 'Transfer Received'),
    )

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"


# ==========================
# Loan Model
# ==========================
class Loan(models.Model):

    LOAN_TYPES = (
        ('Personal Loan', 'Personal Loan'),
        ('Home Loan', 'Home Loan'),
        ('Education Loan', 'Education Loan'),
    )

    STATUS_TYPES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    loan_type = models.CharField(max_length=50, choices=LOAN_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_TYPES, default='Pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.pk:
            old_loan = Loan.objects.get(pk=self.pk)
            if old_loan.status != 'Approved' and self.status == 'Approved':
                self.account.balance += self.amount
                self.account.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.loan_type} - {self.account.user.username}"