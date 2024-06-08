from django.db import models
from django.contrib.auth.models import User



class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=10, unique=True)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return self.user.username

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('Deposit', 'Deposit'),
        ('Withdrawal', 'Withdrawal'),
        ('Transfer', 'Transfer'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    account_number = models.AutoField(primary_key=True)  # Auto-incrementing field, acts as the account number
    avg_amouny = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def calculate_avg_last_10_transactions(self):
        transactions = Transaction.objects.filter(account__user=self.user).order_by('-timestamp')[:10]
        total_amount = sum(transaction.amount for transaction in transactions)
        avg_amount = total_amount / len(transactions) if len(transactions) > 0 else 0.0
        return avg_amount

    def save(self, *args, **kwargs):
        # Update avg_amouny before saving the instance
        self.avg_amouny = self.calculate_avg_last_10_transactions()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.account_number}"
