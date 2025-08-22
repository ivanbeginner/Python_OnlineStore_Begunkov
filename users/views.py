from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, logout

from users.forms import RegistrationForm, LoginForm


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
    form = LoginForm(request.POST)
    if request.method=='POST':
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            password = data['password']
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('users:home')


    return render(request,'users/login.html',{'form':form})

def logout_user(request):
    logout(request)
    return render(request,'users/logout.html')
def home(request):
    return render(request,'users/home.html')