#!/usr/bin/env python
"""
Initial setup script for NovaCart e-commerce platform.
Handles database migrations and creates sample data.
"""

import os
import sys
import django
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecomstore.settings')
django.setup()

from django.core.management import call_command
from django.contrib.auth import get_user_model
from shop.models import Product
from decimal import Decimal


def main():
    print("=" * 60)
    print("NovaCart Setup")
    print("=" * 60)

    # Run migrations
    print("\n[1/3] Running database migrations...")
    call_command('migrate', verbosity=0)
    print("✓ Migrations applied")

    # Create sample products
    print("\n[2/3] Creating sample products...")
    sample_products = [
        {
            'name': 'Aurora Headphones',
            'description': 'Immersive sound with a comfortable over-ear design for long study sessions.',
            'price': Decimal('89.99'),
            'category': 'Audio',
            'stock': 12,
        },
        {
            'name': 'Nova Smartwatch',
            'description': 'Track your workouts and stay connected with a sleek health-focused display.',
            'price': Decimal('129.50'),
            'category': 'Wearables',
            'stock': 8,
        },
        {
            'name': 'Lumen Laptop Stand',
            'description': 'A sturdy, adjustable stand that improves posture and saves desk space.',
            'price': Decimal('44.00'),
            'category': 'Accessories',
            'stock': 15,
        },
        {
            'name': 'Echo Bluetooth Speaker',
            'description': 'Portable rich bass speaker perfect for home parties and travel.',
            'price': Decimal('59.90'),
            'category': 'Audio',
            'stock': 10,
        },
    ]
    
    created_count = 0
    for item in sample_products:
        product, created = Product.objects.get_or_create(name=item['name'], defaults=item)
        if created:
            created_count += 1
    
    print(f"✓ {created_count} sample products created")

    # Create superuser
    print("\n[3/3] Admin account...")
    User = get_user_model()
    if User.objects.filter(username='admin').exists():
        print("✓ Admin user already exists (admin@example.com)")
    else:
        User.objects.create_superuser('admin', 'admin@example.com', 'password123')
        print("✓ Admin user created")
        print("  Username: admin")
        print("  Password: password123")

    print("\n" + "=" * 60)
    print("Setup complete!")
    print("=" * 60)
    print("\nTo start the development server, run:")
    print("  python manage.py runserver")
    print("\nThen open: http://127.0.0.1:8000/")
    print("\nAdmin panel: http://127.0.0.1:8000/admin/")
    print("=" * 60)


if __name__ == '__main__':
    main()
