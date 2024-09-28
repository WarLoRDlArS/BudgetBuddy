from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate
from django.http import HttpResponse

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(password)
        
        if not (User.objects.filter(username=username).exists()): 
            messages.error(request, 'Invalid User Name')
            return redirect('users:login')
        
        user = authenticate(username=username, password=password) 
        
        if user is None:
            messages.error(request, 'Invalid Password')
            return redirect('users:login')
        else:
            login(request, user)
            return redirect('tracking:dashboard')

    return render(request, 'users/loginpage.html')


from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from tracking.models import Category

def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if user already exists
        user = User.objects.filter(username=username)
        if user.exists():
            messages.error(request, 'User Already Exists')
            return redirect('users:register')

        # Create the user
        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()
        
        # Create default categories for the new user
        default_categories = [
            {'catname': 'Groceries', 'description': 'Daily grocery expenses'},
            {'catname': 'Utilities', 'description': 'Monthly utility bills'},
            {'catname': 'Entertainment', 'description': 'Leisure and entertainment expenses'}, 
        ]

        for category in default_categories:
            Category.objects.create(
                user=user,
                catname=category['catname'],
                description=category['description'],
                essential=False  # You can set this based on your needs
            )

        # Create a default account for the user
        Account.objects.create(
            user=user,
            account_type='Personal',
            account_description='Default account for personal expenses'
        )

        messages.info(request, 'Registration Successful')
        return redirect('users:login')


@login_required(login_url='users:login')
def logout_user(request):
    logout(request=request)
    return redirect('users:login')