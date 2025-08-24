
from django.urls import path

from users.views import home, register, login_user,logout_user

app_name = 'users'
urlpatterns = [
    path('',home,name='home'),
    path('login/',login_user,name='login'),
    path('logout/',logout_user,name='logout'),
    path('registration/',register,name = 'register')
]