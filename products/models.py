
from django.db import models
# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    category = models.ForeignKey('Category', on_delete=models.PROTECT)

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

