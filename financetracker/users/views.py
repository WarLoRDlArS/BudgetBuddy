from django.shortcuts import render

# Create your views here.

from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not (Users.objects.filter(username=username).exists()): 
            messages.error(request, 'Invalid User Name')
            return redirect('users:login')
        
        user = authenticate(user=username, password=password)

        if user is None:
            messages.error(request, 'Invalid Password')
            return redirect('users:login')
        else:
            login(request, user)
            return redirect('home')
    
    return render(request, 'users/loginpage.html')


def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username)

        if user.exists():
            messages.error(request, 'User Already Exists')
            return redirect('users:register')

        user = User.objects.create(username=username)
        user.set_password(password=password)
        user.save()
        messages.info(request, 'Registration Successful')
        return redirect('')
    
    return render(request, 'user/registrationpage.html')