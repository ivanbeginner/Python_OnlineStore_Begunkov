from django import forms

from basket.forms import CartForm


# Create your models here.
class OrderForm(forms.Form):
    name = forms.CharField()
    address = forms.CharField()
    email = forms.EmailField()
