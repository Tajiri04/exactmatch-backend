from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class Category(models.Model):
    """Unified category system for all types of battery categorization"""
    
    CATEGORY_TYPE_CHOICES = [
        ('vehicle_type', 'Vehicle Type'),  # SUV, Truck, Small Car, Matatu
        ('battery_type', 'Battery Type'),  # AGM, Maintenance-Free, Flooded, Lithium
        ('use_case', 'Use Case'),         # Private Car, Matatu, Truck, Solar/Backup
        ('brand_series', 'Brand Series'), # For brand-specific series
    ]
    
    name = models.CharField(max_length=100)
    category_type = models.CharField(max_length=20, choices=CATEGORY_TYPE_CHOICES, 
                                   default='vehicle_type',
                                   help_text="Type of categorization this represents")
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                                      related_name='subcategories',
                                      help_text="For hierarchical categories")
    
    # Display settings
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0, help_text="Order for display")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['category_type', 'display_order', 'name']

    def __str__(self):
        return f"{self.get_category_type_display()}: {self.name}"

class Brand(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    country = models.CharField(max_length=100, blank=True, help_text="Country of origin")
    is_popular = models.BooleanField(default=False, help_text="Mark as popular brand")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Battery(models.Model):
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('used', 'Used'),
        ('refurbished', 'Refurbished'),
    ]
    
    VOLTAGE_CHOICES = [
        ('12V', '12 Volt'),
        ('24V', '24 Volt'),
        ('6V', '6 Volt'),
    ]

    # Basic Information
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='batteries')
    
    # Enhanced Categorization - Multiple categories for different purposes
    categories = models.ManyToManyField(Category, related_name='batteries', blank=True,
                                      help_text="Multiple categories (vehicle type, battery type, use case)")
    
    # Enhanced Vehicle Compatibility - This is the killer feature!
    compatible_vehicles = models.JSONField(default=list, blank=True, 
                                         help_text="List of compatible vehicle models e.g., ['Toyota Vitz', 'Mazda Demio', 'Nissan March']")
    
    # Vehicle compatibility search helpers
    vehicle_makes = models.JSONField(default=list, blank=True,
                                   help_text="List of vehicle makes e.g., ['Toyota', 'Mazda', 'Nissan']")
    vehicle_models = models.JSONField(default=list, blank=True,
                                    help_text="List of specific models e.g., ['Vitz', 'Demio', 'March']")
    
    model_number = models.CharField(max_length=100, unique=True)
    
    # Technical Specifications
    voltage = models.CharField(max_length=10, choices=VOLTAGE_CHOICES, default='12V')
    amp_hours = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(1000)])
    cold_cranking_amps = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(2000)])
    reserve_capacity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(500)])
    
    # Physical Specifications
    length = models.DecimalField(max_digits=6, decimal_places=2, help_text="Length in cm")
    width = models.DecimalField(max_digits=6, decimal_places=2, help_text="Width in cm")
    height = models.DecimalField(max_digits=6, decimal_places=2, help_text="Height in cm")
    weight = models.DecimalField(max_digits=6, decimal_places=2, help_text="Weight in kg")
    
    # Commercial Information
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='new')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    
    # Description and Media
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    features = models.JSONField(default=list, blank=True, help_text="List of battery features")
    compatibility = models.JSONField(default=list, blank=True, help_text="Compatible car models")
    
    # SEO and Display
    slug = models.SlugField(max_length=250, unique=True)
    is_featured = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Seller Information
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='batteries_for_sale')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_featured', 'is_active']),
            models.Index(fields=['is_popular', 'is_active']),
            models.Index(fields=['brand', 'is_active']),
            models.Index(fields=['price', 'is_active']),
            models.Index(fields=['voltage', 'is_active']),
        ]

    def __str__(self):
        return f"{self.brand.name} {self.name} - {self.model_number}"

    @property
    def discount_percentage(self):
        if self.original_price and self.original_price > self.price:
            return round(((self.original_price - self.price) / self.original_price) * 100)
        return 0

    @property
    def is_in_stock(self):
        return self.stock_quantity > 0

class BatteryImage(models.Model):
    battery = models.ForeignKey(Battery, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='batteries/')
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"Image for {self.battery.name}"

class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    battery = models.ForeignKey(Battery, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='battery_reviews')
    rating = models.IntegerField(choices=RATING_CHOICES)
    title = models.CharField(max_length=200)
    comment = models.TextField()
    is_verified_purchase = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['battery', 'user']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.battery.name} ({self.rating}/5)"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Totals
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Shipping Information
    shipping_address = models.TextField()
    shipping_city = models.CharField(max_length=100)
    shipping_postal_code = models.CharField(max_length=20)
    shipping_country = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shipped_at = models.DateTimeField(blank=True, null=True)
    delivered_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    battery = models.ForeignKey(Battery, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.battery.name}"

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    battery = models.ForeignKey(Battery, on_delete=models.CASCADE, related_name='wishlisted_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'battery']

    def __str__(self):
        return f"{self.user.username} - {self.battery.name}"
