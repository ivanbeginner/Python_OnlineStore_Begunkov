from django.db import models

from basket.cart import Cart
from basket.forms import CartForm
from django.contrib.auth import get_user_model
User = get_user_model()


class Order(models.Model):
    name = models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.CharField()
    email = models.EmailField()
    cart = models.JSONField()
    def __str__(self):
        return f'Order - {self.pk}'
