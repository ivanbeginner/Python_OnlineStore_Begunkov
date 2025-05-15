from django.urls import path
from orders.views import create_order
app_name = 'orders'
urlpatterns = [
    path('create_order/',create_order,name='create_order')
]