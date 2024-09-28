from django import forms
from .models import Category, Account, Transaction

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['description', 'catname', 'essential']

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['account_type', 'account_description']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'description', 'transaction_type', 'date', 'category', ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        } 
