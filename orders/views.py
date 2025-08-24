from django.contrib.auth import get_user_model

from django.shortcuts import render, redirect
from django.contrib import messages
from basket.models import CartAndUser, CartAndProduct

from orders.forms import OrderForm
from orders.models import Order
from products.models import Product, StockBalance

User = get_user_model()


# Create your views here.

def stock_balance(cart_products):
    """Обновление количества товаров на складе и в StockBalance"""
    for cart in cart_products:
        product = Product.objects.filter(pk=cart.product_id)
        product_quantity = product.last().quantity
        product.update(quantity=product_quantity-cart.quantity)
        StockBalance.objects.update_or_create(product=product.last(),defaults={'quantity':product.last().quantity})


def create_order(request):
    """Создание заказа"""
    if request.method=='POST':
        order_form = OrderForm(request.POST)
        if not request.user.is_authenticated:
            return redirect('users:login')
        cart = CartAndUser.objects.filter(user_id=request.user.id).last()
        cart_products = CartAndProduct.objects.filter(cart_id=cart.pk)
        if len(cart_products) == 0 or not cart_products:
            messages.error(request, 'Ваша корзина пуста')
            return redirect('cart:cart_detail')
        price = sum(item.products_price() for item in cart_products)


        if order_form.is_valid():
            #Подставляем данные из формы
            data = order_form.cleaned_data
            order = Order.objects.create(user_id = request.user.id,
                          address=data['address'],
                          email=data['email'],cart_id = cart.pk, total_cost=price)

            order.save()
            stock_balance(cart_products)
            #После заказа создаем новую пустую корзину
            CartAndUser.objects.create(user_id=request.user.id)
            return redirect('orders:order_detail',str(order.id))
    else:
        order_form = OrderForm()
    return render(request,'orders/order.html',{'form':order_form})

def order_detail(request,order_id):
    """Детали заказа"""
    if not request.user.is_authenticated:
        return redirect('users:login')
    order = Order.objects.filter(pk=order_id).last()
    if not order:
        messages.error(request,'Нет заказа с таким номером')
        return redirect('orders:order_list')

    cart_products = CartAndProduct.objects.filter(cart_id=order.cart_id)
    products = {}
    for cart_item in cart_products:
        product = Product.objects.filter(id=cart_item.product_id).first()
        products[product.name]=cart_item.quantity

    return render(request,'orders/order_detail.html',context={'products':products,'order':order})

def orders_list(request):
    """Список заказов пользователя"""
    if not request.user.is_authenticated:
        return redirect('users:login')
    orders = Order.objects.filter(user_id=request.user.id)
    return render(request,'orders/order_list.html',{'orders':orders})