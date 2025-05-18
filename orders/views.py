from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from basket.models import Cart
from orders.forms import OrderForm
from orders.models import Order

User = get_user_model()


# Create your views here.


class OrderView(LoginRequiredMixin):
    pass

def create_order(request):
    cart = Cart.objects.filter(user_id=request.user.id)
    if not cart:
        messages.error(request,'Ваша корзина пуста')
        return redirect('cart:cart_detail')
    if request.method=='POST':
        order_form = OrderForm(request.POST)
        user = User.objects.get(id=request.user.id)
        if order_form.is_valid():
            order = Order(user_id = user.id if request.user.is_authenticated else None,
                          address=order_form.cleaned_data['address'],
                          email=order_form.cleaned_data['email'],cart = {'cart':[item.id for item in cart]})

            order.save()


        messages.success(request,'Заказ офрмлен успешно')
    else:
        order_form = OrderForm()
    return render(request,'orders/order.html',{'form':order_form})

