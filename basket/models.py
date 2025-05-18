
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


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    session_key = models.CharField(max_length=32,null=True,blank=True)
    quantity = models.PositiveIntegerField()
    class Meta:
        db_table = 'cart'
        verbose_name = 'Cart'
        verbose_name_plural = 'Cart'

    objects = CartQueryset().as_manager()
    def products_price(self):
        return round(self.product.price * self.quantity)



