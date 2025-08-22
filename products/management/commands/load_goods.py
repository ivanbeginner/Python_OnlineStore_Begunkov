from django.core.management.base import BaseCommand
from django.core.management import call_command
from products.models import Product, StockBalance
import json


class Command(BaseCommand):
    help = 'Load goods data from JSON file'

    def handle(self, *args, **options):

        call_command('loaddata', 'data.json')


        for product in Product.objects.all():
            StockBalance.objects.update_or_create(product=product, defaults={'quantity': 0})

        self.stdout.write(self.style.SUCCESS('Successfully loaded goods data'))