from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from basket.models import Cart
from orders.forms import OrderForm
from orders.models import Order
from products.models import Product

User = get_user_model()


# Create your views here.


class OrderView(LoginRequiredMixin):
    pass

def create_order(request):
    cart = Cart.objects.filter(user_id=request.user.id)
    products_and_quantity = {}

    if not cart:
        messages.error(request,'Ваша корзина пуста')
        return redirect('cart:cart_detail')
    if request.method=='POST':
        if request.user.is_authenticated:
            order_form = OrderForm(request.POST)

            if order_form.is_valid():
                data = order_form.cleaned_data
                order = Order.objects.create(user_id = request.user.id if request.user.is_authenticated else None,
                              address=data['address'],
                              email=data['email'],cart = {'cart':[item.id for item in cart]})

                cart = Cart.objects.delete(user_id=request.user.id)


                cart.save()
                order.save()


            messages.success(request,'Заказ оформлен успешно')
            return redirect('orders:order_detail')
        else:
            redirect('users:registration')
    else:
        order_form = OrderForm()
    return render(request,'orders/order.html',{'form':order_form})

def order_detail(request):

    order = Order.objects.filter(user_id=request.user.id)

    products = {}
    for cart_item in order[len(order)-1].cart['cart']:
        cart = Cart.objects.filter(id=cart_item).first()
        print(cart)
        product = Product.objects.filter(id=cart.product.pk).first()
        products[product.name]=cart.quantity
    print(products)
    return render(request,'orders/order_detail.html',context={'products':products})
