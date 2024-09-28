from django.shortcuts import render,redirect
from .forms import CategoryForm, AccountForm, TransactionForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404,redirect

from .models import Category
from django.db.models import Sum
from .models import Transaction
from django.utils import timezone
from datetime import timedelta, datetime
 

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



from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta

def get_net_income(user, year=None, month=None):
    """
    Calculate the net income for the given user for the specified month and year.
    """
    # Get the current date
    now = timezone.now()
    
    if year and month:
        # Calculate the first and last day of the specified month
        first_day_of_month = timezone.datetime(year, month, 1)
        last_day_of_month = (first_day_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    else:
        # Default to the current month
        first_day_of_month = now.replace(day=1)
        last_day_of_month = (first_day_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    
    total_expense = Transaction.objects.filter(
        user=user,
        transaction_type='expense',
        date__range=[first_day_of_month, last_day_of_month]
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    total_income = Transaction.objects.filter(
        user=user,
        transaction_type='income',
        date__range=[first_day_of_month, last_day_of_month]
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    net_income = total_income - total_expense
    return net_income, total_expense, total_income


@login_required(login_url="users:login")
def dashboard(request):
    current_year = datetime.now().year
    years = [year for year in range(current_year - 5, current_year + 1)]

    months = [
        {'value': '01', 'display': 'January'},
        {'value': '02', 'display': 'February'},
        {'value': '03', 'display': 'March'},
        {'value': '04', 'display': 'April'},
        {'value': '05', 'display': 'May'},
        {'value': '06', 'display': 'June'},
        {'value': '07', 'display': 'July'},
        {'value': '08', 'display': 'August'},
        {'value': '09', 'display': 'September'},
        {'value': '10', 'display': 'October'},
        {'value': '11', 'display': 'November'},
        {'value': '12', 'display': 'December'},
    ]
    
    selected_month = request.GET.get('month')
    selected_year = request.GET.get('year')
    selected_category = request.GET.get('category')

    month = int(selected_month) if selected_month else None
    year = int(selected_year) if selected_year else None

    net_income, total_expense, total_income = get_net_income(user=request.user, year=year, month=month)

    filter_kwargs = {'user': request.user}
    if year:
        filter_kwargs['date__year'] = year
    if month:
        filter_kwargs['date__month'] = month
    if selected_category:
        filter_kwargs['category_id'] = selected_category

    transactions = Transaction.objects.filter(**filter_kwargs).order_by('-date')

    categories = Category.objects.filter(user=request.user)  # Fetch user's categories

    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'net_income': net_income,
        'transactions': transactions,
        'months': months,
        'years': years,
        'categories': categories,  # Pass categories to the template
    }

    return render(request, 'tracking/dashboard.html', context=context)


@login_required(login_url="users:login")
def delete_transaction(request,pk):
    transaction = get_object_or_404(Transaction,id=pk, user=request.user)
    
    if request.method == 'POST':
        transaction.delete()
        return redirect('tracking:dashboard')
    
    return render(request, 'tracking/confirm_delete.html', {'transaction': transaction})

@login_required(login_url="users:login")
def edit_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)
    
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('tracking:dashboard')  # Redirect to the dashboard after saving
    else:
        form = TransactionForm(instance=transaction)
    
    return render(request, 'tracking/editTransaction.html', {'form': form, 'transaction': transaction})