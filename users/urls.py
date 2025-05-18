
from django.urls import path

from users.views import home, RegisterView, register, login_user

app_name = 'users'
urlpatterns = [
    path('',home,name='home'),
     path('login/',login_user,name='login'),
    # path('logout/'),
    path('registration/',register,name = 'register')
]