from django.shortcuts import render,redirect
from .forms import CategoryForm, AccountForm, TransactionForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Category
from django.db.models import Sum
from .models import Transaction

 
@login_required(login_url="users:login")
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)   
            category.user = request.user         
            category.save()                     
            return redirect('tracking:dashboard')  
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
    categories = Category.objects.filter(user=request.user)
    
    if request.method == 'POST':
        print(request.POST)  # This will show you the submitted form data
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user  
            transaction.save()
            # print(transaction)
            return redirect('tracking:dashboard')
        else:
            print("Form is invalid")
            print(form.errors)  # Print out form errors for debugging
    else:
        form = TransactionForm()

    return render(request, 'tracking/createTransaction.html', context={'form': form, 'categories': categories})



def get_net_income(user):
    """
    Calculate the net income for the given user.
    """
    total_income = Transaction.objects.filter(user=user, transaction_type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = Transaction.objects.filter(user=user, transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    net_income = total_income - total_expense
    return net_income

def get_net_expense(user):
    """
    Calculate the net expense for the given user.
    """
    total_expense = Transaction.objects.filter(user=user, transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    return total_expense

@login_required(login_url = "users:login")
def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    context = {
        'net_income': get_net_income(request.user),
        'get_net_expense': get_net_expense(request.user),
        'transactions': transactions,
    }
    return render(request,'tracking/dashboard.html', context=context)

@login_required(login_url="users:login")
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, id=pk, user=request.user)
    
    if request.method == 'POST':
        transaction.delete()
        return redirect('tracking:dashboard')
    
    return render(request, 'tracking/confirm_delete.html', {'transaction': transaction})