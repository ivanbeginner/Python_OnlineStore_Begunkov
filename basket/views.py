from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404

from basket.models import Cart
from basket.forms import CartForm

from products.models import Product
from django.views.decorators.http import require_POST


@require_POST
def add_to_cart(request,product_id):
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
    return redirect('users:login')
@require_POST
def cart_remove(request,product_id):
    product = Product.objects.get(pk=product_id)
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, product=product)
        if carts.exists():
            cart = carts.first()
            cart.delete()

    return redirect('cart:cart_detail')
@require_POST
def delete_item(request,product_id):
    product = Product.objects.get(pk=product_id)
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, product=product)
        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity -= 1
                cart.save()
        else:
            return redirect('cart:cart_detail')
    return redirect('cart:cart_detail')
def cart_detail(request):
    cart = Cart.objects.filter(user_id=request.user.id)
    price = sum(item.products_price() for item in cart )

    print(f'user - {request.user.id}')
    print(price)


    return render(request,'basket/cart.html',{'cart':cart,'price':price})

