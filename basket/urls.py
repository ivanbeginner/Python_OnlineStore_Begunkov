from django.urls import path

from basket.views import add_to_cart, cart_detail, cart_remove, delete_item

app_name = 'cart'
urlpatterns = [
    path('cart_detail/',cart_detail,name='cart_detail'),
    path('add_to_cart/<int:product_id>/',add_to_cart,name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/',cart_remove,name='remove_from_cart'),
    path('delete_item/<int:product_id>/',delete_item,name='delete_item')
]