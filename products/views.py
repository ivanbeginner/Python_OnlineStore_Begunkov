
# Create your views here.
from django.shortcuts import render, get_object_or_404

from basket.forms import CartForm
from products.models import Product

def product_list(request):
	products = Product.objects.all()
	context = {'products': products}
	return render(request, 'products/product_list.html', context)

def product_detail(request, pk):
	product = get_object_or_404(Product,id=pk)
	cart_product_form = CartForm()
	return render(request, 'products/product_detail.html', {'product': product,
                                                        'cart_product_form': cart_product_form})