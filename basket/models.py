
from django import forms
from products.models import Product

class Basket(forms.Form):
	product = forms.ModelChoiceField(queryset=Product.objects.all())
	quantity = forms.IntegerField()
