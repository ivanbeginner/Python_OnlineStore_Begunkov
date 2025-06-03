from django.urls import path
from orders.views import create_order, order_detail

app_name = 'orders'
urlpatterns = [
    path('create_order/',create_order,name='create_order'),
    path('order_detail/',order_detail,name='order_detail')
]