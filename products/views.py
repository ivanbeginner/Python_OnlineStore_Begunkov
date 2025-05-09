
# Create your views here.
from django.shortcuts import render
from products.models import Product

def product_list(request):
	products = Product.objects.all()
	context = {'products': products}
	return render(request, 'products/product_list', context)

def product_detail(request, pk):
	product = Product.objects.get(pk=pk)
	context = {'product': product}
	return render(request, 'product_detail.html', context)