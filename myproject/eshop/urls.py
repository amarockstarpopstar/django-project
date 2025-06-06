from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views
from .api import ProductViewSet, CategoryViewSet, TagViewSet
from .views import AddProductView, EditProductView, DeleteProductView

router = DefaultRouter()
router.register(r'api/products', ProductViewSet)
router.register(r'api/categories', CategoryViewSet)
router.register(r'api/tags', TagViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/add/', AddProductView.as_view(), name='add_product'),
    path('product/<int:product_id>/edit/', EditProductView.as_view(), name='edit_product'),
    path('product/<int:pk>/delete/', DeleteProductView.as_view(), name='delete_product'),
    
    # Category URLs
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:category_id>/', views.category_detail, name='category_detail'),
    path('categories/add/', views.add_category, name='add_category'),
    
    # Tag URLs
    path('tags/', views.tag_list, name='tag_list'),
    path('tags/<int:tag_id>/', views.tag_detail, name='tag_detail'),
    path('tags/add/', views.add_tag, name='add_tag'),
    
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('order/', views.order, name='order'),
    path('orders/confirmed/', views.confirmed_orders, name='confirmed_orders'),
    path('about/', views.about, name='about'),
    path('api/', views.api_docs, name='api_docs'),
    path('profile/', views.profile, name='profile'),
    
    # User authentication URLs
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]

urlpatterns += router.urls