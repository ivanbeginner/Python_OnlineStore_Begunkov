
from django.db import models
# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(upload_to='')
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ['name']
        indexes = [ models.Index(fields=['id']), models.Index(fields=['name'])]
    def __str__(self):
     return self.name

class Category(models.Model):
    name = models.CharField(max_length=255)
    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['name'])]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
     return self.name


class StockBalance(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='stock')
    quantity = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} шт."

    class Meta:
        verbose_name = 'Остаток товара'
        verbose_name_plural = 'Остатки товаров'