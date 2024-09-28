from django import forms
from .models import Income, Expense


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount', 'description']
        widgets = {
            'description': forms.TextInput(attrs={'placeholder': 'Describe your income'}),
            'amount': forms.NumberInput(attrs={'placeholder': 'Enter amount'}),
        }

# Form for inputting expenses
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'description']
        widgets = {
            'description': forms.TextInput(attrs={'placeholder': 'Describe your expense'}),
            'amount': forms.NumberInput(attrs={'placeholder': 'Enter amount'}),
        }