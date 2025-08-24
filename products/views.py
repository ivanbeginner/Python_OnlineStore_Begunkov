
# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from basket.forms import CartForm
from products.models import Product
import logging

def product_list(request):
	"""Список товаров"""
	products = Product.objects.all()
	return render(request,'products/base.html',{'products':products})


def product_detail(request, pk):
	"""Информация о товаре"""
	product = get_object_or_404(Product,id=pk)
	cart_product_form = CartForm()
	return render(request, 'products/product_detail.html', {'product': product,
                                                        'cart_product_form': cart_product_form})