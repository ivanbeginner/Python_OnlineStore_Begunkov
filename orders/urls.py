from django.urls import path
from orders.views import create_order, order_detail, orders_list

app_name = 'orders'
urlpatterns = [
    path('create_order/',create_order,name='create_order'),
    path('order_detail/<int:order_id>',order_detail,name='order_detail'),
    path('order_list/',orders_list,name='order_list')
]