from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from basket.models import CartAndUser, CartAndProduct
from basket.forms import CartForm

from products.models import Product
from django.views.decorators.http import require_POST


def login_check(request):
    if not request.user.is_authenticated:
        return redirect('users:login')
    return True
def update_product_quantity(request,cart_products):
    if cart_products:
        for cart_product in cart_products:
            products = Product.objects.filter(pk=cart_product.product_id)
            product_quantity = products.last().quantity
            quantity_in_cart = cart_product.quantity
            if quantity_in_cart > product_quantity:
                messages.error(request, f'Добавьте меньше позиций <{products.last().name}>(максимум {product_quantity})')
                return redirect('cart:cart_detail')
            products.update(quantity=product_quantity - quantity_in_cart)

def add_to_cart(request,product_id):
    if login_check(request):
        product = Product.objects.get(pk=product_id)
        carts_users = CartAndUser.objects.filter(user_id=request.user.id).last()

        if not carts_users:
            carts_users=CartAndUser.objects.create(user_id=request.user.id)


        carts_products = CartAndProduct.objects.filter(cart_id=carts_users.pk, product_id=product.id)
        if not carts_products:
            create_cart_products=CartAndProduct.objects.create(cart_id=carts_users.pk,product_id=product.id,quantity=0)
            print(create_cart_products.quantity)

        quantity = carts_products.last().quantity
        print(quantity)

        quantity+=1
        if quantity>product.quantity:
            messages.error(request, f'Количество товара <{product.name}> ограничено (максимум {product.quantity})')
            return redirect('cart:cart_detail')
        carts_products.update(quantity=quantity)
        return redirect('cart:cart_detail')


def remove_from_cart(request,product_id):
    if login_check(request):
        product = Product.objects.get(pk=product_id)
        if not request.user.is_authenticated:
            return redirect('users:login')
        cart = CartAndUser.objects.filter(user_id=request.user.id).last()
        CartAndProduct.objects.filter(cart_id=cart.pk,product=product.id).delete()
        return redirect('cart:cart_detail')

def delete_item(request,product_id):
    if login_check(request):
        product = Product.objects.get(pk=product_id)
        cart = CartAndUser.objects.filter(user_id=request.user.id).last()
        cart = CartAndProduct.objects.filter(cart_id=cart.pk,product_id=product.id)
        if cart:
            quantity = cart.last().quantity
            quantity -=1
            cart.update(quantity=quantity)
            if cart.last().quantity==0:
                remove_from_cart(request,product_id)
    return redirect('cart:cart_detail')
def cart_detail(request):

    if login_check(request):
        cart_user = CartAndUser.objects.filter(user=request.user.id).last()
        if not cart_user:
            CartAndUser.objects.create(user_id=request.user.id)
            cart_user = CartAndUser.objects.filter(user=request.user.id).last()
        cart = CartAndProduct.objects.filter(cart=cart_user.id).order_by('product_id')

        price = sum(item.products_price() for item in cart )

        return render(request,'basket/cart.html',{'cart':cart,'price':price})

