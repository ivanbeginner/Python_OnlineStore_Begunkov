from django.shortcuts import render, redirect
from basket.models import Basket

def add_to_cart(request):
    if request.method == 'POST':
        form = Basket(request.POST)
        if form.is_valid():
            product = form.clean_data['product']
            quantity = form.clean_data['quantity']
            cart, created = Basket.objects.get_or_create(user=request.user)
            cart.add_item(product, quantity)
            return redirect('cart')
    else:
        form = Basket()
    return render(request, 'add_to_cart.html', {'form': form})