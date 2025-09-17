#!/usr/bin/env python
import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nickyg_computers.settings')
django.setup()

from ecommerce.models import Category, Product, Service
from django.contrib.auth.models import User

def create_sample_data():
    # Create superuser
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@nickygcomputers.com', 'admin123')
        print("Superuser created: admin/admin123")

    # Create categories
    categories_data = [
        {'name': 'Computers', 'slug': 'computers', 'description': 'Desktop computers and laptops'},
        {'name': 'Phones', 'slug': 'phones', 'description': 'Smartphones and mobile devices'},
        {'name': 'Accessories', 'slug': 'accessories', 'description': 'Computer and phone accessories'},
        {'name': 'Stationary', 'slug': 'stationary', 'description': 'Office and school supplies'},
    ]
    
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            slug=cat_data['slug'],
            defaults=cat_data
        )
        if created:
            print(f"Created category: {category.name}")

    # Get categories
    computers_cat = Category.objects.get(slug='computers')
    phones_cat = Category.objects.get(slug='phones')
    accessories_cat = Category.objects.get(slug='accessories')
    stationary_cat = Category.objects.get(slug='stationary')

    # Create sample products
    products_data = [
        {
            'id': 'laptop-hp-001',
            'name': 'HP Pavilion 15 Laptop',
            'category': computers_cat,
            'sub_category': 'laptops',
            'brand': 'HP',
            'price': 3500.00,
            'short_description': 'Powerful laptop for work and entertainment',
            'long_description': 'HP Pavilion 15 with Intel Core i5 processor, 8GB RAM, 256GB SSD, and 15.6-inch Full HD display. Perfect for students and professionals.',
            'stock': 5,
            'is_featured': True,
            'processor': 'Intel Core i5',
            'ram': '8GB',
            'storage': '256GB SSD',
            'screen_size': '15.6 inch'
        },
        {
            'id': 'phone-samsung-001',
            'name': 'Samsung Galaxy A54',
            'category': phones_cat,
            'sub_category': 'smartphones',
            'brand': 'Samsung',
            'price': 1800.00,
            'short_description': 'Feature-rich smartphone with excellent camera',
            'long_description': 'Samsung Galaxy A54 with 128GB storage, 6GB RAM, triple camera system, and long-lasting battery.',
            'stock': 8,
            'is_featured': True,
            'storage': '128GB',
            'ram': '6GB',
        },
        {
            'id': 'desktop-dell-001',
            'name': 'Dell OptiPlex Desktop',
            'category': computers_cat,
            'sub_category': 'desktops',
            'brand': 'Dell',
            'price': 2800.00,
            'short_description': 'Reliable desktop computer for office use',
            'long_description': 'Dell OptiPlex desktop with Intel Core i3, 4GB RAM, 500GB HDD, perfect for office work and basic computing needs.',
            'stock': 3,
            'is_featured': False,
            'processor': 'Intel Core i3',
            'ram': '4GB',
            'storage': '500GB HDD',
        },
        {
            'id': 'phone-iphone-001',
            'name': 'iPhone 12',
            'category': phones_cat,
            'sub_category': 'smartphones',
            'brand': 'Apple',
            'price': 4200.00,
            'short_description': 'Premium iPhone with advanced features',
            'long_description': 'iPhone 12 with 128GB storage, A14 Bionic chip, dual camera system, and 5G connectivity.',
            'stock': 2,
            'is_featured': True,
            'storage': '128GB',
        },
        {
            'id': 'accessory-mouse-001',
            'name': 'Wireless Mouse',
            'category': accessories_cat,
            'sub_category': 'peripherals',
            'brand': 'Logitech',
            'price': 85.00,
            'short_description': 'Ergonomic wireless mouse',
            'long_description': 'Logitech wireless mouse with ergonomic design, long battery life, and precise tracking.',
            'stock': 15,
            'is_featured': False,
        },
        {
            'id': 'accessory-keyboard-001',
            'name': 'Mechanical Keyboard',
            'category': accessories_cat,
            'sub_category': 'peripherals',
            'brand': 'Corsair',
            'price': 320.00,
            'short_description': 'RGB mechanical gaming keyboard',
            'long_description': 'Corsair mechanical keyboard with RGB backlighting, tactile switches, and durable construction.',
            'stock': 7,
            'is_featured': False,
        },
        {
            'id': 'stationary-notebook-001',
            'name': 'Exercise Books (Pack of 10)',
            'category': stationary_cat,
            'sub_category': 'books',
            'brand': 'Local',
            'price': 25.00,
            'short_description': 'Quality exercise books for students',
            'long_description': 'Pack of 10 quality exercise books, 80 pages each, suitable for all school subjects.',
            'stock': 50,
            'is_featured': False,
        },
        {
            'id': 'stationary-pens-001',
            'name': 'Ballpoint Pens (Pack of 12)',
            'category': stationary_cat,
            'sub_category': 'writing',
            'brand': 'Bic',
            'price': 18.00,
            'short_description': 'Reliable ballpoint pens',
            'long_description': 'Pack of 12 Bic ballpoint pens in blue ink, smooth writing and long-lasting.',
            'stock': 30,
            'is_featured': False,
        }
    ]

    for product_data in products_data:
        product, created = Product.objects.get_or_create(
            id=product_data['id'],
            defaults=product_data
        )
        if created:
            print(f"Created product: {product.name}")

    # Create sample services
    services_data = [
        {
            'id': 'service-repair-001',
            'name': 'Computer Repair',
            'category': 'IT',
            'description': 'Professional repair services for desktops and laptops, troubleshooting hardware and software issues.',
            'duration_estimate': '1-3 hours',
            'price_range': '50-200 GH₵',
            'availability': 'Walk-in, Mon-Sat',
            'icon': 'fas fa-wrench',
            'is_featured': True
        },
        {
            'id': 'service-internet-001',
            'name': 'Internet Cafe',
            'category': 'DIGITAL',
            'description': 'High-speed internet access, computer usage, printing, and scanning services.',
            'duration_estimate': 'Hourly rates',
            'price_range': '2-5 GH₵ per hour',
            'availability': 'Daily, 7am-10pm',
            'icon': 'fas fa-wifi',
            'is_featured': True
        },
        {
            'id': 'service-waec-001',
            'name': 'WAEC Registration',
            'category': 'EDUCATION',
            'description': 'NOV/DEC WAEC registration and form filling services.',
            'duration_estimate': '30 minutes',
            'price_range': '20-50 GH₵',
            'availability': 'Registration periods',
            'icon': 'fas fa-graduation-cap',
            'is_featured': True
        },
        {
            'id': 'service-passport-001',
            'name': 'Passport Photos',
            'category': 'BUSINESS',
            'description': 'Professional passport and document photography services.',
            'duration_estimate': '10 minutes',
            'price_range': '5-15 GH₵',
            'availability': 'Daily',
            'icon': 'fas fa-camera',
            'is_featured': True
        },
        {
            'id': 'service-typing-001',
            'name': 'Document Typing',
            'category': 'BUSINESS',
            'description': 'Professional document typing, formatting, and printing services.',
            'duration_estimate': 'Varies',
            'price_range': '1-5 GH₵ per page',
            'availability': 'Daily',
            'icon': 'fas fa-file-alt',
            'is_featured': True
        },
        {
            'id': 'service-momo-001',
            'name': 'Mobile Money Services',
            'category': 'BUSINESS',
            'description': 'Mobile money transactions, cash-in, cash-out, and transfer services.',
            'duration_estimate': '2-5 minutes',
            'price_range': 'Standard rates',
            'availability': 'Daily',
            'icon': 'fas fa-mobile-alt',
            'is_featured': True
        }
    ]

    for service_data in services_data:
        service, created = Service.objects.get_or_create(
            id=service_data['id'],
            defaults=service_data
        )
        if created:
            print(f"Created service: {service.name}")

    print("\nSample data creation completed!")
    print("Admin login: admin / admin123")
    print("Visit /admin/ to manage the site")

if __name__ == '__main__':
    create_sample_data()
