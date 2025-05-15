
from django.urls import path

from users.views import home, RegisterView, register

app_name = 'users'
urlpatterns = [
    path('',home,name='home'),
    # path('login/',),
    # path('logout/'),
    path('registration/',register,name = 'register')
]