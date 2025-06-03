from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import RegistrationForm

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('users:home')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})


def login_user(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('users:home')
        else:
            return render(request,'users/login.html',{'error_message':'Invalid login'})
    else:
        return render(request,'users/login.html')

def logout_user(request):
    logout(request)
    return render(request,'users/logout.html')
def home(request):
    return render(request,'users/home.html')