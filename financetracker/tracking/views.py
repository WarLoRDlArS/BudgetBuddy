from django.shortcuts import render,redirect
from .forms import CategoryForm, AccountForm, TransactionForm
from django.contrib.auth.decorators import login_required


@login_required(login_url = "users:login")
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tracking: dashboard')  
    else:
        form = CategoryForm()
    return render(request, 'tracking/createCategory.html', {'form': form})


@login_required(login_url = "users:login")
def create_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user  # Associate account with the logged-in user
            account.save()
            return redirect('tracking:dashboard')
    else:
        form = AccountForm()
    return render(request, 'tracking/createAccount.html', context={'form': form})


@login_required(login_url='users:login')
def create_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user  
            transaction.save()
            return redirect('tracking:dashboard')
    else:
        form = TransactionForm()
    return render(request, 'tracking/createTransaction.html', context={'form': form})


@login_required(login_url = "users:login")
def dashboard(request):
    return render(request,'tracking/dashboard.html')

