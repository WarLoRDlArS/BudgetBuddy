from django.shortcuts import render,redirect
from .forms import IncomeForm, ExpenseForm
from .models import Income, Expense
from django.contrib.auth.decorators import login_required


@login_required(login_url = "users:login")
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            ##income.user = request.user  
            ##income.save()
            
    else:
        form = IncomeForm()

    return render(request, 'tracking/add_income.html', {'form': form})


@login_required(login_url = "users:login")
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            ##expense.user = request.user 
            ##expense.save()
             
    else:
        form = ExpenseForm()

    return render(request, 'tracking/add_expense.html', {'form': form})



@login_required(login_url = "users:login")
def dashboard(request):
    return render(request,'tracking/dashboard.html')


# Create your views here.
