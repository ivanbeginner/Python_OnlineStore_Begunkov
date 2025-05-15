"""
URL configuration for onlinestore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from products.urls import urlpatterns as product_urls
from basket.urls import urlpatterns as cart_patterns
from orders.urls import urlpatterns as order_patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('products.urls',namespace='products')),
    path('cart/',include('basket.urls',namespace='cart')),
    path('orders/',include('orders.urls',namespace='orders')),
    path('users/',include('users.urls',namespace='users'))
]
