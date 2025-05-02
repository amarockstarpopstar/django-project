from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/add/', views.add_product, name='add_product'),
    path('product/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    
    # Category URLs
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:category_id>/', views.category_detail, name='category_detail'),
    path('categories/add/', views.add_category, name='add_category'),
    
    # Tag URLs
    path('tags/', views.tag_list, name='tag_list'),
    path('tags/<int:tag_id>/', views.tag_detail, name='tag_detail'),
    path('tags/add/', views.add_tag, name='add_tag'),
    
    path('cart/', views.cart, name='cart'),
    path('about/', views.about, name='about'),
    path('api/', views.api_docs, name='api_docs'),
    path('profile/', views.profile, name='profile'),
] 