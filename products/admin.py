from django.contrib import admin

# Register your models here.
from django.contrib import admin
from products.models import Product, Category

# admin.site.register(Product)
# admin.site.register(Category)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','description','price','image','category']
    list_filter = ['price','category']
