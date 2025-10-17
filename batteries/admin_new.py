from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Battery, BatteryImage, Brand, Category,
    Review, Order, OrderItem, Wishlist
)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'is_popular', 'website', 'created_at']
    search_fields = ['name', 'country']
    readonly_fields = ['created_at']
    list_filter = ['country', 'is_popular', 'created_at']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_type', 'parent_category', 'is_active', 'display_order', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['category_type', 'is_active', 'parent_category']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['category_type', 'display_order', 'name']

class BatteryImageInline(admin.TabularInline):
    model = BatteryImage
    extra = 1
    fields = ['image', 'alt_text', 'is_primary', 'order']

@admin.register(Battery)
class BatteryAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'brand', 'model_number', 'voltage', 'price', 
        'stock_quantity', 'condition', 'is_featured', 'is_popular', 'is_active'
    ]
    list_filter = [
        'brand', 'categories', 'voltage', 'condition', 
        'is_featured', 'is_popular', 'is_active'
    ]
    search_fields = ['name', 'model_number', 'brand__name', 'description', 'compatible_vehicles']
    readonly_fields = ['id', 'slug', 'created_at', 'updated_at', 'discount_percentage', 'is_in_stock']
    filter_horizontal = ['categories']  # Nice widget for many-to-many
    inlines = [BatteryImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'name', 'brand', 'model_number', 'slug')
        }),
        ('Categorization & Compatibility', {
            'fields': ('categories', 'compatible_vehicles', 'vehicle_makes', 'vehicle_models'),
            'description': 'Use categories for filtering (vehicle type, battery type, use case) and compatibility for exact vehicle matching.'
        }),
        ('Technical Specifications', {
            'fields': ('voltage', 'amp_hours', 'cold_cranking_amps', 'reserve_capacity')
        }),
        ('Physical Specifications', {
            'fields': ('length', 'width', 'height', 'weight')
        }),
        ('Commercial Information', {
            'fields': ('condition', 'price', 'original_price', 'stock_quantity', 'seller')
        }),
        ('Description & Features', {
            'fields': ('description', 'short_description', 'features', 'compatibility')
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'is_popular', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('brand')

@admin.register(BatteryImage)
class BatteryImageAdmin(admin.ModelAdmin):
    list_display = ['battery', 'alt_text', 'is_primary', 'order']
    list_filter = ['is_primary', 'battery__brand']
    search_fields = ['battery__name', 'alt_text']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['battery', 'user', 'rating', 'title', 'is_verified_purchase', 'created_at']
    list_filter = ['rating', 'is_verified_purchase', 'created_at']
    search_fields = ['battery__name', 'user__username', 'title', 'comment']
    readonly_fields = ['created_at', 'updated_at']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['total_price']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['order_number', 'user__username', 'shipping_address']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'battery', 'quantity', 'unit_price', 'total_price']
    list_filter = ['order__status']
    search_fields = ['order__order_number', 'battery__name']

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'battery', 'created_at']
    search_fields = ['user__username', 'battery__name']
    readonly_fields = ['created_at']
