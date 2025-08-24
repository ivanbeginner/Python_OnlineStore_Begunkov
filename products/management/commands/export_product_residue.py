from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Export product residue data to JSON'

    def handle(self, *args, **options):
        call_command('dumpdata', 'products.StockBalance', '--indent', '4', '--output', 'stock_data.json')
        self.stdout.write(self.style.SUCCESS('Successfully exported product residue data'))