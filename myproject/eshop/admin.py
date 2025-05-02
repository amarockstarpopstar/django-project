from django.contrib import admin

# Register your models here.
from .models import Category, Tag, Product, Order, OrderPosition

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass

@admin.register(OrderPosition)
class OrderPositionAdmin(admin.ModelAdmin):
    pass

