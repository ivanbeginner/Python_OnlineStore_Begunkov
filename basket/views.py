from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404

from basket.models import Cart
from basket.forms import CartForm

from products.models import Product
from django.views.decorators.http import require_POST









@require_POST
def add_to_cart(request,product_id):
    # cart = Cart(request)
    # product = get_object_or_404(Product,id=product_id)
    # form = CartForm(request.POST)
    # if form.is_valid():
    #     cd = form.cleaned_data
    #     cart.add(product=product,quantity=cd['quantity'],update_quantity=cd['update'])
    # return redirect('cart:cart_detail')

    # return render(request, 'basket/add_to_basket.html', {'form': form})
    product = Product.objects.get(pk=product_id)
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user,product=product)
        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity+=1
                cart.save()
        else:
            Cart.objects.create(user=request.user,product=product,quantity=1)
    return redirect('cart:cart_detail')
@require_POST
def cart_remove(request,product_id):
    cart = Cart(request)
    product = get_object_or_404(Product,id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')
@require_POST
def delete_item(request,product_id):
    cart = Cart(request)
    product = get_object_or_404(Product,id=product_id)
    cart.delete_item(product)
    return redirect('cart:cart_detail')
def cart_detail(request):
    cart = Cart.objects.get(user_id=request.user.id)
    for item in cart:
        return item
    return render(request,'basket/cart.html',{'cart':cart})

