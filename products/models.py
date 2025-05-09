
from django.db import models
# Create your models here.


class Product(models.Model):
     product_id = models.UUIDField(max_length=15,primary_key=True)
     name = models.CharField(max_length=255)
     description = models.TextField()
     price = models.DecimalField(max_digits=7, decimal_places=2)
     image = models.ImageField(upload_to='products/')
     category = models.ForeignKey('Category', on_delete=models.PROTECT)

     def str(self):
         return [self.name]

class Category(models.Model):
   name = models.CharField(max_length=255)

   def str(self):
     return [self.name]

