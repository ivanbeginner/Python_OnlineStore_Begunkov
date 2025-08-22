

from django.shortcuts import render, redirect, get_object_or_404

from basket.models import CartAndUser, CartAndProduct
from basket.forms import CartForm

from products.models import Product
from django.views.decorators.http import require_POST



def add_to_cart(request,product_id):
    product = Product.objects.get(pk=product_id)

    if request.user.is_authenticated:
        carts_users = CartAndUser.objects.filter(user_id=request.user.id).last()

        if not carts_users:
            carts_users=CartAndUser.objects.create(user_id=request.user.id)


        carts_products = CartAndProduct.objects.filter(cart_id=carts_users.pk, product_id=product.id)
        if not carts_products:
            CartAndProduct.objects.create(cart_id=carts_users.pk,product_id=product.id,quantity=1)

        else:
            cart = carts_users
            cart_and_product = CartAndProduct.objects.filter(cart_id=cart.pk,product_id=product.id)
            quantity = cart_and_product.last().quantity
            quantity+=1
            cart_and_product.update(quantity=quantity)
        return redirect('cart:cart_detail')
    return redirect('users:login')

def cart_remove(request,product_id):
    product = Product.objects.get(pk=product_id)
    if request.user.is_authenticated:
        cart = CartAndUser.objects.filter(user_id=request.user.id).last()
        CartAndProduct.objects.filter(cart_id=cart.pk,product=product.id).delete()

    return redirect('cart:cart_detail')

def delete_item(request,product_id):
    product = Product.objects.get(pk=product_id)
    if request.user.is_authenticated:
        cart = CartAndUser.objects.filter(user_id=request.user.id).last()
        cart = CartAndProduct.objects.filter(cart_id=cart.pk,product_id=product.id)
        if cart:
            quantity = cart.last().quantity
            quantity -=1
            cart.update(quantity=quantity)
        else:
            return redirect('cart:cart_detail')
    return redirect('cart:cart_detail')
def cart_detail(request):
    if request.user.is_authenticated:
        cart_user = CartAndUser.objects.filter(user=request.user.id).last()
        if not cart_user:
            CartAndUser.objects.create(user_id=request.user.id)
            cart_user = CartAndUser.objects.filter(user=request.user.id).last()
        cart = CartAndProduct.objects.filter(cart=cart_user.id)
        price = sum(item.products_price() for item in cart )


        return render(request,'basket/cart.html',{'cart':cart,'price':price})
    return redirect('users:login')
