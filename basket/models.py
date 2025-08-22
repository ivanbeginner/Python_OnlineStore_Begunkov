from decimal import Decimal
from django.db import models

from products.models import Product
from users.models import User



class CartQueryset(models.QuerySet):
    def total_price(self):
        return sum([cart.products_price() for cart in self])
    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class CartAndUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        db_table = 'cart_and_user'
        verbose_name = 'CartAndUser'
        verbose_name_plural = 'CartsAndeUsers'

class CartAndProduct(models.Model):
    cart = models.ForeignKey(CartAndUser,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        db_table='cart_and_product'
        verbose_name='CartAndProduct'
        verbose_name_plural = 'CartsAndProducts'


    def products_price(self):
        return round(self.quantity*self.product.price)