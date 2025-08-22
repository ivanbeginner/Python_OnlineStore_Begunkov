from django.db import models
from basket.models import CartAndUser
from basket.forms import CartForm
from django.contrib.auth import get_user_model
User = get_user_model()


class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.CharField()
    email = models.EmailField(default='')
    cart = models.ForeignKey(CartAndUser,on_delete=models.CASCADE,default=0)
    class Meta:
        db_table = 'orders'
        verbose_name = 'order'
        verbose_name_plural = 'orders'

    def __str__(self):
        return f'Order - {self.pk}'
