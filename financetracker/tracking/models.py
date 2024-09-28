from django.db import models
from django.contrib.auth.models import User

# Create your models here. 


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    description = models.TextField()
    catname = models.CharField(max_length=255)
    essential = models.BooleanField(default=False)

    def __str__(self):
        return self.catname


class Account(models.Model):
    account_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    account_type = models.CharField(max_length=255)
    account_description = models.TextField()

    def __str__(self):
        return f"{self.account_type} ({self.user.username})"


class TransactionType(models.Model):
    transaction_type_id = models.AutoField(primary_key=True)
    description = models.TextField() 

    def __str__(self):
        return self.description
 

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    date = models.DateField()
    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPE_CHOICES)

    def __str__(self):
        return f"{self.transaction_type.capitalize()}: {self.amount} - {self.description}"



class CustomDate(models.Model):
    date = models.DateField(primary_key=True)

    def __str__(self):
        return str(self.date)
