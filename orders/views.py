from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from basket.models import CartAndUser, CartAndProduct
from orders.forms import OrderForm
from orders.models import Order
from products.models import Product, StockBalance

User = get_user_model()


# Create your views here.


class OrderView(LoginRequiredMixin):
    pass

def create_order(request):

    if request.method=='POST':
        if not request.user.is_authenticated:
            return redirect('users:login')
        cart = CartAndUser.objects.filter(user_id=request.user.id).last()
        cart_products = CartAndProduct.objects.filter(cart_id=cart.pk)
        price = sum(item.products_price() for item in cart_products)

        if not cart:
            messages.error(request, 'Ваша корзина пуста')
            return redirect('cart:cart_detail')
        order_form = OrderForm(request.POST)

        if order_form.is_valid():
            for cart_product in cart_products:
                products = Product.objects.filter(pk=cart_product.product_id)
                product_quantity = products.last().quantity
                quantity_in_cart = cart_product.quantity
                if quantity_in_cart>product_quantity:
                    messages.error(request, f'Добавьте меньше позиций <{products.last().name}>(максимум {product_quantity})')
                    return redirect('cart:cart_detail')
                products.update(quantity=product_quantity-quantity_in_cart)
            data = order_form.cleaned_data
            order = Order.objects.create(user_id = request.user.id if request.user.is_authenticated else None,
                          address=data['address'],
                          email=data['email'],cart_id = cart.pk, total_cost=price)

            order.save()
            products = Product.objects.all()
            for product in products:
                StockBalance.objects.filter(product_id=product.id).update(quantity=product.quantity)
            CartAndUser.objects.create(user_id=request.user.id)
            messages.success(request,'Заказ оформлен успешно')
            return redirect('orders:order_detail',str(order.id))
    else:
        order_form = OrderForm()
    return render(request,'orders/order.html',{'form':order_form})

def order_detail(request,order_id):
    order = Order.objects.filter(pk=order_id).last()
    print(order.status)
    cart_products = CartAndProduct.objects.filter(cart_id=order.cart_id)
    products = {}
    for cart_item in cart_products:
        product = Product.objects.filter(id=cart_item.product_id).first()
        products[product.name]=cart_item.quantity
    print(products)
    return render(request,'orders/order_detail.html',context={'products':products,'order':order})

def orders_list(request):
    orders = Order.objects.filter(user_id=request.user.id)
    return render(request,'orders/order_list.html',{'orders':orders})