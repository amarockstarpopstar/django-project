from django.shortcuts import render, redirect

# Homepage view
def home(request):
    return render(request, 'eshop/home.html', {'title': 'Главная страница'})

# Catalog view
def catalog(request):
    # Sample products data
    products = [
        {'id': 1, 'name': 'Товар 1', 'price': 1000, 'image': 'https://via.placeholder.com/150'},
        {'id': 2, 'name': 'Товар 2', 'price': 2000, 'image': 'https://via.placeholder.com/150'},
        {'id': 3, 'name': 'Товар 3', 'price': 3000, 'image': 'https://via.placeholder.com/150'},
    ]
    return render(request, 'eshop/catalog.html', {'title': 'Каталог', 'products': products})

# Product detail view
def product_detail(request, product_id):
    # Sample product data (in real app, this would be fetched from a database)
    product = {
        'id': product_id,
        'name': f'Товар {product_id}',
        'price': 1000 * product_id,
        'description': f'Подробное описание товара {product_id}',
        'image': 'https://via.placeholder.com/300',
    }
    return render(request, 'eshop/product_detail.html', {'title': product['name'], 'product': product})

# Add product view
def add_product(request):
    if request.method == 'POST':
        # Here would be form processing and database save
        return redirect('catalog')
    return render(request, 'eshop/add_product.html', {'title': 'Добавление товара'})

# Edit product view
def edit_product(request, product_id):
    # Sample product data to edit
    product = {
        'id': product_id,
        'name': f'Товар {product_id}',
        'price': 1000 * product_id,
        'description': f'Подробное описание товара {product_id}',
        'image': 'https://via.placeholder.com/300',
        'category': 'Электроника',
    }
    
    if request.method == 'POST':
        # Here would be form processing and database update
        return redirect('product_detail', product_id=product_id)
    
    return render(request, 'eshop/edit_product.html', {'title': 'Изменение товара', 'product': product})

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
    orders = [
        {
            'id': 101,
            'date': '2023-04-15',
            'status': 'Доставлен',
            'total': 5000,
            'items': [
                {'name': 'Товар 1', 'quantity': 2, 'price': 1000},
                {'name': 'Товар 2', 'quantity': 1.5, 'price': 2000},
            ]
        },
        {
            'id': 102,
            'date': '2023-04-10',
            'status': 'В обработке',
            'total': 3000,
            'items': [
                {'name': 'Товар 3', 'quantity': 1, 'price': 3000},
            ]
        },
    ]
    
    return render(request, 'eshop/profile.html', {'title': 'Личный кабинет', 'user': user, 'orders': orders})
