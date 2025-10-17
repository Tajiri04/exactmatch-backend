from django.shortcuts import render
from django.db.models import Q, Avg
from rest_framework import generics, filters, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.reverse import reverse
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters_rf

from .models import (
    Battery, Brand, Category, Review, Order, OrderItem, Wishlist
)
from .serializers import (
    BatteryListSerializer, BatteryDetailSerializer, BrandSerializer,
    CategorySerializer, ReviewSerializer, CreateReviewSerializer,
    OrderSerializer, CreateOrderSerializer, WishlistSerializer,
    UserSerializer
)

# ✅ Pagination
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 50

# ✅ Battery Filters
class BatteryFilter(filters_rf.FilterSet):
    min_price = filters_rf.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters_rf.NumberFilter(field_name="price", lookup_expr='lte')
    brand = filters_rf.CharFilter(field_name="brand__name", lookup_expr='icontains')
    category = filters_rf.CharFilter(field_name="categories__name", lookup_expr='icontains')
    categories = filters_rf.BaseInFilter(field_name="categories__id", lookup_expr='in')
    category_type = filters_rf.ChoiceFilter(field_name="categories__category_type", choices=Category.CATEGORY_TYPE_CHOICES)
    voltage = filters_rf.ChoiceFilter(choices=Battery.VOLTAGE_CHOICES)
    condition = filters_rf.ChoiceFilter(choices=Battery.CONDITION_CHOICES)
    min_amp_hours = filters_rf.NumberFilter(field_name="amp_hours", lookup_expr='gte')
    max_amp_hours = filters_rf.NumberFilter(field_name="amp_hours", lookup_expr='lte')
    min_cca = filters_rf.NumberFilter(field_name="cold_cranking_amps", lookup_expr='gte')
    max_cca = filters_rf.NumberFilter(field_name="cold_cranking_amps", lookup_expr='lte')
    in_stock = filters_rf.BooleanFilter(method='filter_in_stock')
    vehicle_search = filters_rf.CharFilter(method='filter_vehicle_compatibility')
    
    class Meta:
        model = Battery
        fields = ['is_featured', 'is_popular', 'brand']
    
    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock_quantity__gt=0)
        return queryset
    
    def filter_vehicle_compatibility(self, queryset, name, value):
        return queryset.filter(
            Q(compatible_vehicles__icontains=value) |
            Q(vehicle_makes__icontains=value) |
            Q(vehicle_models__icontains=value)
        )

# ✅ Battery Views
class BatteryListView(generics.ListAPIView):
    queryset = Battery.objects.filter(is_active=True).select_related('brand').prefetch_related('categories')
    serializer_class = BatteryListSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BatteryFilter
    search_fields = ['name', 'model_number', 'brand__name', 'description', 'short_description', 'compatible_vehicles']
    ordering_fields = ['price', 'created_at', 'name', 'amp_hours', 'cold_cranking_amps']
    ordering = ['-created_at']

class FeaturedBatteriesView(generics.ListAPIView):
    queryset = Battery.objects.filter(is_active=True, is_featured=True).select_related('brand').prefetch_related('categories')
    serializer_class = BatteryListSerializer
    pagination_class = StandardResultsSetPagination

class PopularBatteriesView(generics.ListAPIView):
    queryset = Battery.objects.filter(is_active=True, is_popular=True).select_related('brand').prefetch_related('categories')
    serializer_class = BatteryListSerializer
    pagination_class = StandardResultsSetPagination

class BatteryDetailView(generics.RetrieveAPIView):
    queryset = Battery.objects.filter(is_active=True).select_related('brand', 'seller').prefetch_related('categories', 'images', 'reviews')
    serializer_class = BatteryDetailSerializer
    lookup_field = 'slug'

# ✅ Brands & Categories
class BrandListView(generics.ListAPIView):
    queryset = Brand.objects.all().order_by('name')
    serializer_class = BrandSerializer

class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    
    def get_queryset(self):
        category_type = self.request.query_params.get('type', None)
        parent_id = self.request.query_params.get('parent', None)
        
        queryset = Category.objects.filter(is_active=True)
        
        if category_type:
            queryset = queryset.filter(category_type=category_type)
        if parent_id:
            queryset = queryset.filter(parent_category_id=parent_id)
        elif parent_id is None and not category_type:
            queryset = queryset.filter(parent_category__isnull=True)
        
        return queryset.order_by('display_order', 'name')

# ✅ Reviews
class BatteryReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        battery_id = self.kwargs['battery_id']
        return Review.objects.filter(battery_id=battery_id).select_related('user')

class CreateReviewView(generics.CreateAPIView):
    serializer_class = CreateReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

# ✅ Orders
class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items__battery')

class CreateOrderView(generics.CreateAPIView):
    serializer_class = CreateOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items__battery')

# ✅ Wishlist
class WishlistView(generics.ListAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user).select_related('battery__brand').prefetch_related('battery__categories')

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_to_wishlist(request):
    battery_id = request.data.get('battery_id')
    try:
        battery = Battery.objects.get(id=battery_id, is_active=True)
        wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, battery=battery)
        if created:
            return Response({'message': 'Battery added to wishlist'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Battery already in wishlist'}, status=status.HTTP_200_OK)
    except Battery.DoesNotExist:
        return Response({'error': 'Battery not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def remove_from_wishlist(request, battery_id):
    try:
        wishlist_item = Wishlist.objects.get(user=request.user, battery_id=battery_id)
        wishlist_item.delete()
        return Response({'message': 'Battery removed from wishlist'}, status=status.HTTP_204_NO_CONTENT)
    except Wishlist.DoesNotExist:
        return Response({'error': 'Battery not in wishlist'}, status=status.HTTP_404_NOT_FOUND)

# ✅ Search & Dashboard
@api_view(['GET'])
def search_suggestions(request):
    query = request.GET.get('q', '')
    if len(query) < 2:
        return Response([])
    
    batteries = Battery.objects.filter(
        Q(name__icontains=query) |
        Q(brand__name__icontains=query) |
        Q(model_number__icontains=query),
        is_active=True
    ).select_related('brand')[:10]
    
    suggestions = [
        {'text': f"{b.brand.name} {b.name}", 'type': 'battery', 'slug': b.slug}
        for b in batteries
    ]
    for brand in Brand.objects.filter(name__icontains=query)[:5]:
        suggestions.append({'text': brand.name, 'type': 'brand', 'slug': brand.name.lower().replace(' ', '-')})
    
    return Response(suggestions)

@api_view(['GET'])
def dashboard_stats(request):
    stats = {
        'total_batteries': Battery.objects.filter(is_active=True).count(),
        'featured_batteries': Battery.objects.filter(is_active=True, is_featured=True).count(),
        'popular_batteries': Battery.objects.filter(is_active=True, is_popular=True).count(),
        'total_brands': Brand.objects.count(),
        'total_categories': Category.objects.count(),
        'in_stock_batteries': Battery.objects.filter(is_active=True, stock_quantity__gt=0).count(),
    }
    return Response(stats)

@api_view(['GET'])
def battery_specifications(request, battery_id):
    try:
        battery = Battery.objects.get(id=battery_id, is_active=True)
        specs = {
            'technical': {
                'voltage': battery.voltage,
                'amp_hours': battery.amp_hours,
                'cold_cranking_amps': battery.cold_cranking_amps,
                'reserve_capacity': battery.reserve_capacity,
            },
            'physical': {
                'length': float(battery.length),
                'width': float(battery.width),
                'height': float(battery.height),
                'weight': float(battery.weight),
            },
            'features': battery.features,
            'compatibility': battery.compatibility,
        }
        return Response(specs)
    except Battery.DoesNotExist:
        return Response({'error': 'Battery not found'}, status=status.HTTP_404_NOT_FOUND)

# ✅ API Root
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'batteries': {
            'list': reverse('battery-list', request=request, format=format),
            'featured': reverse('featured-batteries', request=request, format=format),
            'popular': reverse('popular-batteries', request=request, format=format),
        },
        'brands': reverse('brand-list', request=request, format=format),
        'categories': reverse('category-list', request=request, format=format),
        'orders': reverse('order-list', request=request, format=format),
        'wishlist': reverse('wishlist', request=request, format=format),
        'dashboard': reverse('dashboard-stats', request=request, format=format),
    })
