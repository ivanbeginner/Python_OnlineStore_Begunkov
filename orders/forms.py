from django import forms

from basket.forms import CartForm


# Create your models here.
class OrderForm(forms.Form):
    name = forms.CharField(label='Введите ваше имя')
    address = forms.CharField(label='Введите адрес')
    email = forms.EmailField(label='Введите email')
