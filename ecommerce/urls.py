from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('products/<str:product_id>/', views.product_detail, name='product_detail'),
    path('services/', views.services, name='services'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # Cart functionality (AJAX endpoints)
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/', views.update_cart, name='update_cart'),
    
    # Order functionality
    path('order/place/', views.place_order, name='place_order'),
    
    # Search
    path('search/', views.search_products, name='search_products'),
    
    # Admin login redirect
    path('admin-login/', views.admin_login_redirect, name='admin_login_redirect'),
]
