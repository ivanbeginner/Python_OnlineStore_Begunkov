from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from basket.models import CartAndUser, CartAndProduct
from basket.forms import CartForm

from products.models import Product
from django.views.decorators.http import require_POST




def add_to_cart(request,product_id):
    """Добавление товара в корзину"""
    if not request.user.is_authenticated:
        return redirect('users:login')
    product = Product.objects.get(pk=product_id)
    carts_users = CartAndUser.objects.filter(user_id=request.user.id).last()

    #Если нет корзины, то создаем ее
    if not carts_users:
        carts_users=CartAndUser.objects.create(user_id=request.user.id)

    #Если нет товаров в корзине, то добавляем товар
    carts_products = CartAndProduct.objects.filter(cart_id=carts_users.pk, product_id=product.id)
    if not carts_products:
        CartAndProduct.objects.create(cart_id=carts_users.pk,product_id=product.id,quantity=0)

    #Если есть товар в корзине, то увеличиваем количество
    quantity = carts_products.last().quantity


    quantity+=1
    #Если количество товара в корзине превышает количество на складе, то выводим сообщение с ошибкой
    if quantity>product.quantity:
        messages.error(request, f'Количество товара <{product.name}> ограничено (максимум {product.quantity})')
        return redirect('cart:cart_detail')
    carts_products.update(quantity=quantity)
    return redirect('cart:cart_detail')


def remove_from_cart(request,product_id):
    """Удаление товара из корзины"""
    if not request.user.is_authenticated:
        return redirect('users:login')
    product = Product.objects.get(pk=product_id)
    if not request.user.is_authenticated:
        return redirect('users:login')
    cart = CartAndUser.objects.filter(user_id=request.user.id).last()
    CartAndProduct.objects.filter(cart_id=cart.pk,product=product.id).delete()
    return redirect('cart:cart_detail')

def delete_item(request,product_id):
    """Уменьшение количества товара в корзине"""
    if not request.user.is_authenticated:
        return redirect('users:login')
    product = Product.objects.get(pk=product_id)
    cart = CartAndUser.objects.filter(user_id=request.user.id).last()
    cart = CartAndProduct.objects.filter(cart_id=cart.pk,product_id=product.id)
    if cart:
        quantity = cart.last().quantity
        quantity -=1
        cart.update(quantity=quantity)
        #Если в корзине количество товара 0, то удаляем его из корзины
        if cart.last().quantity==0:
            remove_from_cart(request,product_id)
    return redirect('cart:cart_detail')
def cart_detail(request):
    """Информация о корзине"""
    if not request.user.is_authenticated:
        return redirect('users:login')
    cart_user = CartAndUser.objects.filter(user=request.user.id).last()
    if not cart_user:
        CartAndUser.objects.create(user_id=request.user.id)
        cart_user = CartAndUser.objects.filter(user=request.user.id).last()
    cart = CartAndProduct.objects.filter(cart=cart_user.id).order_by('product_id')
    price = sum(item.products_price() for item in cart )

    return render(request,'basket/cart.html',{'cart':cart,'price':price})

