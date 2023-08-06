from django.core.management.base import BaseCommand
from souschef.order.factories import OrderFactory


class Command(BaseCommand):
    help = 'Creates a happy bunch of clients with orders'

    def handle(self, *args, **options):
        orders = OrderFactory.create_batch(500, status='D')
        self.stdout.write(
            self.style.SUCCESS(
                'Successfully created client {} orders'.format(orders)
            )
        )
