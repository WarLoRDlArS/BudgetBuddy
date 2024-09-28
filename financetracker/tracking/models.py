from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Income: {self.amount}"

# Model to store expense transactions
class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)