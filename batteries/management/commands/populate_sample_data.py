from django.core.management.base import BaseCommand
from batteries.models import Brand, Category, Battery
from django.contrib.auth.models import User
from django.utils.text import slugify
from decimal import Decimal

class Command(BaseCommand):
    help = 'Populate the database with sample battery data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Get or create a default seller
        seller, created = User.objects.get_or_create(
            username='admin_seller',
            defaults={
                'email': 'admin@exactmatch.com',
                'first_name': 'Admin',
                'last_name': 'Seller',
                'is_staff': True,
            }
        )
        if created:
            seller.set_password('adminpass123')
            seller.save()
            self.stdout.write(f'Created seller: {seller.username}')
        
        # Create Brands
        brands_data = [
            {'name': 'ACDelco', 'description': 'Professional automotive batteries with proven reliability'},
            {'name': 'Optima', 'description': 'High-performance SpiralCell batteries'},
            {'name': 'Interstate', 'description': 'America\'s #1 replacement battery brand'},
            {'name': 'DieHard', 'description': 'Tough batteries for tough conditions'},
            {'name': 'Bosch', 'description': 'German-engineered automotive excellence'},
            {'name': 'Exide', 'description': 'Global leader in energy storage solutions'},
        ]
        
        for brand_data in brands_data:
            brand, created = Brand.objects.get_or_create(
                name=brand_data['name'],
                defaults={'description': brand_data['description']}
            )
            if created:
                self.stdout.write(f'Created brand: {brand.name}')
        
        # Create Categories
        categories_data = [
            {'name': 'AGM', 'description': 'Absorbent Glass Mat batteries for superior performance'},
            {'name': 'Flooded', 'description': 'Traditional lead-acid batteries'},
            {'name': 'SpiralCell', 'description': 'Optima\'s patented spiral cell technology'},
            {'name': 'Gel', 'description': 'Gel electrolyte batteries for deep cycle applications'},
            {'name': 'Lithium', 'description': 'Lightweight lithium-ion automotive batteries'},
        ]
        
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Create Batteries
        batteries_data = [
            {
                'name': 'ACDelco 48AGM Professional',
                'brand': 'ACDelco',
                'category': 'AGM',
                'model_number': 'AC48AGM',
                'price': Decimal('189.99'),
                'voltage': '12V',
                'amp_hours': 70,
                'cold_cranking_amps': 760,
                'reserve_capacity': 120,
                'length': Decimal('27.7'),
                'width': Decimal('17.5'),
                'height': Decimal('19.1'),
                'weight': Decimal('21.0'),
                'description': 'Professional-grade AGM battery with enhanced durability and performance.',
                'short_description': 'Professional AGM battery for superior performance',
                'is_featured': True,
                'stock_quantity': 15,
            },
            {
                'name': 'Optima RedTop 34/78',
                'brand': 'Optima',
                'category': 'SpiralCell',
                'model_number': 'OPT3478',
                'price': Decimal('259.99'),
                'voltage': '12V',
                'amp_hours': 50,
                'cold_cranking_amps': 800,
                'reserve_capacity': 100,
                'length': Decimal('25.4'),
                'width': Decimal('17.5'),
                'height': Decimal('19.8'),
                'weight': Decimal('17.2'),
                'description': 'High-performance starting battery with SpiralCell technology.',
                'short_description': 'High-performance SpiralCell starting battery',
                'is_featured': True,
                'stock_quantity': 8,
            },
            {
                'name': 'Interstate Batteries MTZ-65',
                'brand': 'Interstate',
                'category': 'AGM',
                'model_number': 'INT-MTZ65',
                'price': Decimal('199.99'),
                'voltage': '12V',
                'amp_hours': 75,
                'cold_cranking_amps': 850,
                'reserve_capacity': 140,
                'length': Decimal('30.5'),
                'width': Decimal('17.5'),
                'height': Decimal('19.1'),
                'weight': Decimal('23.3'),
                'description': 'Premium AGM battery with excellent cold cranking performance.',
                'short_description': 'Premium AGM with excellent cold weather performance',
                'is_featured': False,
                'stock_quantity': 12,
            },
            {
                'name': 'DieHard Gold 50748',
                'brand': 'DieHard',
                'category': 'Flooded',
                'model_number': 'DH-50748',
                'price': Decimal('149.99'),
                'voltage': '12V',
                'amp_hours': 65,
                'cold_cranking_amps': 750,
                'reserve_capacity': 120,
                'length': Decimal('30.5'),
                'width': Decimal('17.3'),
                'height': Decimal('22.6'),
                'weight': Decimal('20.0'),
                'description': 'Reliable flooded battery with proven performance.',
                'short_description': 'Reliable traditional flooded battery',
                'is_featured': False,
                'stock_quantity': 20,
            },
            {
                'name': 'Bosch S6 High Performance',
                'brand': 'Bosch',
                'category': 'AGM',
                'model_number': 'BSH-S6HP',
                'price': Decimal('219.99'),
                'voltage': '12V',
                'amp_hours': 80,
                'cold_cranking_amps': 800,
                'reserve_capacity': 150,
                'length': Decimal('30.0'),
                'width': Decimal('17.5'),
                'height': Decimal('19.1'),
                'weight': Decimal('22.0'),
                'description': 'German-engineered AGM battery with premium features.',
                'short_description': 'German-engineered premium AGM battery',
                'is_featured': True,
                'stock_quantity': 6,
            },
            {
                'name': 'Exide Edge FP-AGML4/94R',
                'brand': 'Exide',
                'category': 'AGM',
                'model_number': 'EXD-AGML4',
                'price': Decimal('179.99'),
                'voltage': '12V',
                'amp_hours': 70,
                'cold_cranking_amps': 710,
                'reserve_capacity': 130,
                'length': Decimal('31.5'),
                'width': Decimal('17.5'),
                'height': Decimal('19.1'),
                'weight': Decimal('22.6'),
                'description': 'Flat plate AGM technology for enhanced performance.',
                'short_description': 'Flat plate AGM for enhanced performance',
                'is_featured': False,
                'stock_quantity': 10,
            },
        ]
        
        for battery_data in batteries_data:
            brand = Brand.objects.get(name=battery_data['brand'])
            category = Category.objects.get(name=battery_data['category'])
            
            battery, created = Battery.objects.get_or_create(
                name=battery_data['name'],
                defaults={
                    'brand': brand,
                    'category': category,
                    'model_number': battery_data['model_number'],
                    'price': battery_data['price'],
                    'voltage': battery_data['voltage'],
                    'amp_hours': battery_data['amp_hours'],
                    'cold_cranking_amps': battery_data['cold_cranking_amps'],
                    'reserve_capacity': battery_data['reserve_capacity'],
                    'length': battery_data['length'],
                    'width': battery_data['width'],
                    'height': battery_data['height'],
                    'weight': battery_data['weight'],
                    'description': battery_data['description'],
                    'short_description': battery_data['short_description'],
                    'is_featured': battery_data['is_featured'],
                    'stock_quantity': battery_data['stock_quantity'],
                    'seller': seller,
                    'slug': slugify(battery_data['name']),
                }
            )
            if created:
                self.stdout.write(f'Created battery: {battery.name}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample data!')
        )
