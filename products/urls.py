from django.urls import path

from products.views import  product_detail, ProductView

app_name = 'products'
urlpatterns = [
    path('products/', ProductView.as_view(), name='product_list'),
    path('products/<int:pk>/', product_detail, name='product_detail')

]