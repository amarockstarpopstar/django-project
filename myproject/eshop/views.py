from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm, CategoryForm, TagForm
from .models import Product, Category, Tag, Order, OrderPosition

# Homepage view
def home(request):
    return render(request, 'eshop/home.html', {'title': 'Главная страница'})

# Catalog view
def catalog(request):
    products = Product.objects.filter(is_deleted=False)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    return render(request, 'eshop/catalog.html', {
        'title': 'Каталог', 
        'products': products,
        'categories': categories,
        'tags': tags
    })

# Product detail view
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_deleted=False)
    return render(request, 'eshop/product_detail.html', {'title': product.name, 'product': product})

# Add product view
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalog')
    else:
        form = ProductForm()
    return render(request, 'eshop/add_product.html', {'title': 'Добавление товара', 'form': form})

# Edit product view
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', product_id=product_id)
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'eshop/edit_product.html', {'title': 'Изменение товара', 'form': form, 'product': product})

# Category views
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'eshop/category_list.html', {'title': 'Категории', 'categories': categories})

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category, is_deleted=False)
    return render(request, 'eshop/category_detail.html', {'title': category.name, 'category': category, 'products': products})

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'eshop/add_category.html', {'title': 'Добавление категории', 'form': form})

# Tag views
def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'eshop/tag_list.html', {'title': 'Теги', 'tags': tags})

def tag_detail(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    products = Product.objects.filter(tags=tag, is_deleted=False)
    return render(request, 'eshop/tag_detail.html', {'title': tag.name, 'tag': tag, 'products': products})

def add_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tag_list')
    else:
        form = TagForm()
    return render(request, 'eshop/add_tag.html', {'title': 'Добавление тега', 'form': form})

# Cart view
def cart(request):
    # Sample cart data
    cart_items = [
        {'id': 1, 'name': 'Товар 1', 'price': 1000, 'quantity': 2},
        {'id': 2, 'name': 'Товар 2', 'price': 2000, 'quantity': 1},
    ]
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    return render(request, 'eshop/cart.html', {'title': 'Корзина', 'cart_items': cart_items, 'total': total})

# About page view (Feedback)
def about(request):
    return render(request, 'eshop/about.html', {'title': 'О нас'})

# API documentation view
def api_docs(request):
    # Sample API endpoints
    api_endpoints = [
        {
            'name': 'GET /api/products/',
            'description': 'Получить список всех товаров',
            'params': 'None',
            'response': '{"products": [...]}',
        },
        {
            'name': 'GET /api/products/:id/',
            'description': 'Получить информацию о конкретном товаре',
            'params': 'id - ID товара',
            'response': '{"id": 1, "name": "Товар 1", ...}',
        },
        {
            'name': 'POST /api/products/',
            'description': 'Добавить новый товар',
            'params': 'name, price, description, category',
            'response': '{"id": 3, "name": "Новый товар", ...}',
        },
        {
            'name': 'PUT /api/products/:id/',
            'description': 'Обновить существующий товар',
            'params': 'id, name, price, description, category',
            'response': '{"id": 1, "name": "Обновленный товар", ...}',
        },
        {
            'name': 'DELETE /api/products/:id/',
            'description': 'Удалить товар',
            'params': 'id - ID товара',
            'response': '{"success": true}',
        },
    ]
    return render(request, 'eshop/api_docs.html', {'title': 'API Документация', 'api_endpoints': api_endpoints})

# User profile view
def profile(request):
    # Sample user data
    user = {
        'username': 'user1',
        'email': 'user@example.com',
        'name': 'Иван Иванов',
        'address': 'г. Москва, ул. Примерная, д. 123',
        'phone': '+7 (123) 456-7890',
    }
    
    # Sample orders
    orders = Order.objects.all()
    
    return render(request, 'eshop/profile.html', {'title': 'Личный кабинет', 'user': user, 'orders': orders})
