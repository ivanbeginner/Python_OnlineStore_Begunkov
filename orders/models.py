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
    total_cost = models.IntegerField(default=0)
    class Status(models.TextChoices):
        START='Заказ создан','1'
        PROCESS='В работе','2'
        DONE = 'Завершен','3'
    status = models.CharField(choices=Status.choices,default=Status.START)
    class Meta:
        db_table = 'orders'
        verbose_name = 'order'
        verbose_name_plural = 'orders'

    def __str__(self):
        return f'Order - {self.pk}'
