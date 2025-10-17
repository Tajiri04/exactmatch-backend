from django.urls import path
from . import views

urlpatterns = [
    # Battery endpoints
    path('batteries/', views.BatteryListView.as_view(), name='battery-list'),
    path('batteries/featured/', views.FeaturedBatteriesView.as_view(), name='featured-batteries'),
    path('batteries/popular/', views.PopularBatteriesView.as_view(), name='popular-batteries'),
    path('batteries/<slug:slug>/', views.BatteryDetailView.as_view(), name='battery-detail'),
    path('batteries/<uuid:battery_id>/specifications/', views.battery_specifications, name='battery-specifications'),
    
    # Brand and Category endpoints
    path('brands/', views.BrandListView.as_view(), name='brand-list'),
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    
    # Review endpoints
    path('batteries/<uuid:battery_id>/reviews/', views.BatteryReviewListView.as_view(), name='battery-reviews'),
    path('reviews/create/', views.CreateReviewView.as_view(), name='create-review'),
    
    # Order endpoints
    path('orders/', views.OrderListView.as_view(), name='order-list'),
    path('orders/create/', views.CreateOrderView.as_view(), name='create-order'),
    path('orders/<uuid:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    
    # Wishlist endpoints
    path('wishlist/', views.WishlistView.as_view(), name='wishlist'),
    path('wishlist/add/', views.add_to_wishlist, name='add-to-wishlist'),
    path('wishlist/remove/<uuid:battery_id>/', views.remove_from_wishlist, name='remove-from-wishlist'),
    
    # Search and utilities
    path('search/suggestions/', views.search_suggestions, name='search-suggestions'),
    path('dashboard/stats/', views.dashboard_stats, name='dashboard-stats'),
]
