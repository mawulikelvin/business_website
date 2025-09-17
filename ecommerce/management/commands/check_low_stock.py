from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from ecommerce.models import Product

class Command(BaseCommand):
    help = 'Check for low stock products and send email alerts'

    def add_arguments(self, parser):
        parser.add_argument(
            '--threshold',
            type=int,
            default=5,
            help='Stock threshold for low stock alert (default: 5)',
        )

    def handle(self, *args, **options):
        threshold = options['threshold']
        
        # Find products with low stock
        low_stock_products = Product.objects.filter(
            stock__lte=threshold,
            is_active=True
        )
        
        if low_stock_products.exists():
            try:
                email_subject = f"Low Stock Alert - {low_stock_products.count()} Products Need Restocking"
                email_body = render_to_string('emails/low_stock_alert.html', {
                    'low_stock_products': low_stock_products,
                })
                
                send_mail(
                    subject=email_subject,
                    message='',  # Plain text version
                    html_message=email_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.ADMIN_EMAIL],
                    fail_silently=False,
                )
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Low stock alert sent for {low_stock_products.count()} products'
                    )
                )
                
                for product in low_stock_products:
                    self.stdout.write(f'  - {product.name}: {product.stock} units')
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Failed to send low stock alert: {e}')
                )
        else:
            self.stdout.write(
                self.style.SUCCESS('No low stock products found')
            )
