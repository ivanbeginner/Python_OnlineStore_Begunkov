
# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from basket.forms import CartForm
from products.models import Product
import logging

class ProductView(ListView):
	model = Product
	template_name = 'products/product_list.html'
	context_object_name = 'products'
	def get_queryset(self):
		return Product.objects.all()


def product_detail(request, pk):
	product = get_object_or_404(Product,id=pk)
	cart_product_form = CartForm()
	return render(request, 'products/product_detail.html', {'product': product,
                                                        'cart_product_form': cart_product_form})