from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from batteries.models import Brand, Category, Battery, BatteryImage
from decimal import Decimal
import uuid

class Command(BaseCommand):
    help = 'Populate database with sample battery data using new category system'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data with new category system...')
        
        # Create superuser if it doesn't exist
        admin_user = None
        if not User.objects.filter(is_superuser=True).exists():
            admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Created superuser: admin/admin123'))
        else:
            admin_user = User.objects.filter(is_superuser=True).first()
        
        # Create sample brands
        brands_data = [
            {'name': 'Amaron', 'country': 'India', 'is_popular': True},
            {'name': 'Bosch', 'country': 'Germany', 'is_popular': True}, 
            {'name': 'Chloride Exide', 'country': 'India', 'is_popular': True},
            {'name': 'ACDelco', 'country': 'USA', 'is_popular': False},
            {'name': 'Optima', 'country': 'USA', 'is_popular': False},
            {'name': 'Varta', 'country': 'Germany', 'is_popular': False},
        ]
        
        brands = {}
        for brand_data in brands_data:
            brand, created = Brand.objects.get_or_create(
                name=brand_data['name'],
                defaults=brand_data
            )
            brands[brand.name] = brand
            if created:
                self.stdout.write(f'Created brand: {brand.name}')
        
        # Create categories with the new structure
        categories_data = [
            # Vehicle Types
            {'name': 'Small Cars', 'category_type': 'vehicle_type', 'display_order': 1},
            {'name': 'Sedans', 'category_type': 'vehicle_type', 'display_order': 2},
            {'name': 'SUVs', 'category_type': 'vehicle_type', 'display_order': 3},
            {'name': 'Trucks', 'category_type': 'vehicle_type', 'display_order': 4},
            {'name': 'Motorcycles', 'category_type': 'vehicle_type', 'display_order': 5},
            
            # Battery Types
            {'name': 'Flooded', 'category_type': 'battery_type', 'display_order': 1},
            {'name': 'AGM', 'category_type': 'battery_type', 'display_order': 2},
            {'name': 'Maintenance-Free', 'category_type': 'battery_type', 'display_order': 3},
            {'name': 'Gel', 'category_type': 'battery_type', 'display_order': 4},
            
            # Use Cases
            {'name': 'Daily Driving', 'category_type': 'use_case', 'display_order': 1},
            {'name': 'Heavy Duty', 'category_type': 'use_case', 'display_order': 2},
            {'name': 'Start-Stop Technology', 'category_type': 'use_case', 'display_order': 3},
            {'name': 'Deep Cycle', 'category_type': 'use_case', 'display_order': 4},
            
            # Brand Series
            {'name': 'Go', 'category_type': 'brand_series', 'display_order': 1},
            {'name': 'Current', 'category_type': 'brand_series', 'display_order': 2},
            {'name': 'Pro', 'category_type': 'brand_series', 'display_order': 3},
        ]
        
        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                category_type=cat_data['category_type'],
                defaults=cat_data
            )
            categories[f"{cat_data['category_type']}_{cat_data['name']}"] = category
            if created:
                self.stdout.write(f'Created category: {category.name} ({category.category_type})')
        
        # Create sample batteries with new category relationships
        batteries_data = [
            {
                'name': 'Go 35AH',
                'brand': 'Amaron',
                'model_number': 'AMR-GO-35',
                'slug': 'amaron-go-35ah',
                'voltage': '12V',
                'amp_hours': 35,
                'cold_cranking_amps': 320,
                'reserve_capacity': 70,
                'length': Decimal('20.5'),
                'width': Decimal('17.5'),
                'height': Decimal('19.0'),
                'weight': Decimal('12.5'),
                'price': Decimal('4500.00'),
                'original_price': Decimal('5000.00'),
                'stock_quantity': 25,
                'categories': ['vehicle_type_Small Cars', 'battery_type_Maintenance-Free', 'use_case_Daily Driving', 'brand_series_Go'],
                'compatible_vehicles': ['Maruti Swift', 'Hyundai i10', 'Toyota Etios', 'Tata Nano'],
                'vehicle_makes': ['Maruti', 'Hyundai', 'Toyota', 'Tata'],
                'vehicle_models': ['Swift', 'i10', 'Etios', 'Nano'],
                'is_featured': True,
                'is_popular': True,
                'description': 'Perfect battery for small cars with maintenance-free technology.',
            },
            {
                'name': 'Current 45AH',
                'brand': 'Amaron',
                'model_number': 'AMR-CUR-45',
                'slug': 'amaron-current-45ah',
                'voltage': '12V',
                'amp_hours': 45,
                'cold_cranking_amps': 400,
                'reserve_capacity': 85,
                'length': Decimal('22.0'),
                'width': Decimal('18.0'),
                'height': Decimal('20.0'),
                'weight': Decimal('15.0'),
                'price': Decimal('6200.00'),
                'original_price': Decimal('6800.00'),
                'stock_quantity': 20,
                'categories': ['vehicle_type_Sedans', 'battery_type_Maintenance-Free', 'use_case_Daily Driving', 'brand_series_Current'],
                'compatible_vehicles': ['Honda City', 'Maruti Dzire', 'Hyundai Verna', 'Toyota Yaris'],
                'vehicle_makes': ['Honda', 'Maruti', 'Hyundai', 'Toyota'],
                'vehicle_models': ['City', 'Dzire', 'Verna', 'Yaris'],
                'is_featured': True,
                'is_popular': True,
                'description': 'Reliable battery for sedans with enhanced starting power.',
            },
            {
                'name': 'Pro 55AH',
                'brand': 'Amaron',
                'model_number': 'AMR-PRO-55',
                'slug': 'amaron-pro-55ah',
                'voltage': '12V',
                'amp_hours': 55,
                'cold_cranking_amps': 480,
                'reserve_capacity': 100,
                'length': Decimal('24.0'),
                'width': Decimal('18.5'),
                'height': Decimal('21.0'),
                'weight': Decimal('18.0'),
                'price': Decimal('7800.00'),
                'original_price': Decimal('8500.00'),
                'stock_quantity': 15,
                'categories': ['vehicle_type_SUVs', 'battery_type_Maintenance-Free', 'use_case_Heavy Duty', 'brand_series_Pro'],
                'compatible_vehicles': ['Mahindra XUV500', 'Tata Safari', 'Ford EcoSport', 'Renault Duster'],
                'vehicle_makes': ['Mahindra', 'Tata', 'Ford', 'Renault'],
                'vehicle_models': ['XUV500', 'Safari', 'EcoSport', 'Duster'],
                'is_featured': True,
                'is_popular': False,
                'description': 'High-performance battery designed for SUVs and heavy-duty applications.',
            },
            {
                'name': 'Silver 70AH',
                'brand': 'Bosch',
                'model_number': 'BSH-SLV-70',
                'slug': 'bosch-silver-70ah',
                'voltage': '12V',
                'amp_hours': 70,
                'cold_cranking_amps': 570,
                'reserve_capacity': 120,
                'length': Decimal('25.5'),
                'width': Decimal('19.0'),
                'height': Decimal('22.0'),
                'weight': Decimal('22.0'),
                'price': Decimal('9500.00'),
                'original_price': Decimal('10200.00'),
                'stock_quantity': 12,
                'categories': ['vehicle_type_SUVs', 'battery_type_AGM', 'use_case_Start-Stop Technology'],
                'compatible_vehicles': ['BMW X1', 'Audi Q3', 'Mercedes GLA', 'Volvo XC60'],
                'vehicle_makes': ['BMW', 'Audi', 'Mercedes', 'Volvo'],
                'vehicle_models': ['X1', 'Q3', 'GLA', 'XC60'],
                'is_featured': False,
                'is_popular': True,
                'description': 'Premium AGM battery with start-stop technology support.',
            },
            {
                'name': 'PowerMax 90AH',
                'brand': 'Chloride Exide',
                'model_number': 'EXD-PM-90',
                'slug': 'chloride-exide-powermax-90ah',
                'voltage': '12V',
                'amp_hours': 90,
                'cold_cranking_amps': 720,
                'reserve_capacity': 150,
                'length': Decimal('30.0'),
                'width': Decimal('20.0'),
                'height': Decimal('24.0'),
                'weight': Decimal('28.0'),
                'price': Decimal('11000.00'),
                'original_price': Decimal('12000.00'),
                'stock_quantity': 8,
                'categories': ['vehicle_type_Trucks', 'battery_type_Flooded', 'use_case_Heavy Duty'],
                'compatible_vehicles': ['Ashok Leyland Dost', 'Tata Ace', 'Mahindra Bolero Pickup', 'Force Trax'],
                'vehicle_makes': ['Ashok Leyland', 'Tata', 'Mahindra', 'Force'],
                'vehicle_models': ['Dost', 'Ace', 'Bolero Pickup', 'Trax'],
                'is_featured': False,
                'is_popular': False,
                'description': 'Heavy-duty battery for commercial vehicles and trucks.',
            },
            {
                'name': 'Bike Power 5AH',
                'brand': 'Amaron',
                'model_number': 'AMR-BP-5',
                'slug': 'amaron-bike-power-5ah',
                'voltage': '12V',
                'amp_hours': 5,
                'cold_cranking_amps': 60,
                'reserve_capacity': 15,
                'length': Decimal('11.0'),
                'width': Decimal('7.0'),
                'height': Decimal('10.0'),
                'weight': Decimal('2.5'),
                'price': Decimal('1800.00'),
                'original_price': Decimal('2000.00'),
                'stock_quantity': 30,
                'categories': ['vehicle_type_Motorcycles', 'battery_type_Maintenance-Free', 'use_case_Daily Driving'],
                'compatible_vehicles': ['Honda Activa', 'TVS Jupiter', 'Bajaj Pulsar', 'Hero Splendor'],
                'vehicle_makes': ['Honda', 'TVS', 'Bajaj', 'Hero'],
                'vehicle_models': ['Activa', 'Jupiter', 'Pulsar', 'Splendor'],
                'is_featured': True,
                'is_popular': True,
                'description': 'Compact and reliable battery for motorcycles and scooters.',
            },
        ]
        
        for battery_data in batteries_data:
            # Extract category names and brand
            category_keys = battery_data.pop('categories')
            brand_name = battery_data.pop('brand')
            
            battery, created = Battery.objects.get_or_create(
                name=battery_data['name'],
                brand=brands[brand_name],
                defaults={
                    **battery_data,
                    'brand': brands[brand_name],
                    'seller': admin_user,
                    'condition': 'new',
                    'short_description': battery_data['description'][:100],
                    'features': ['Long lasting', 'Maintenance-free', 'High performance'],
                    'compatibility': f"Compatible with {battery_data['vehicle_makes'][0]} vehicles",
                }
            )
            
            if created:
                # Add categories to the battery
                for cat_key in category_keys:
                    if cat_key in categories:
                        battery.categories.add(categories[cat_key])
                
                self.stdout.write(f'Created battery: {battery.name}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample data!')
        )
        self.stdout.write('Summary:')
        self.stdout.write(f'- Brands: {Brand.objects.count()}')
        self.stdout.write(f'- Categories: {Category.objects.count()}')
        self.stdout.write(f'- Batteries: {Battery.objects.count()}')
        
        # Show category breakdown
        for category_type, _ in Category.CATEGORY_TYPE_CHOICES:
            count = Category.objects.filter(category_type=category_type).count()
            self.stdout.write(f'  - {category_type.replace("_", " ").title()}: {count}')
