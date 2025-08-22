from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from products.views import product_detail, product_list

app_name = 'products'
urlpatterns = [
    path('', product_list, name='product_list'),
    path('products/<int:pk>/', product_detail, name='product_detail')

]
