from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm, CategoryForm, TagForm, UserRegistrationForm, UserLoginForm
from .models import Product, Category, Tag, Order, OrderPosition
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout

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

def get_cart(request):
    """Возвращает корзину из сессии или создает новую."""
    return request.session.setdefault('cart', {})

@require_POST
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    quantity = int(request.POST.get('quantity', 1))
    cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
    request.session['cart'] = cart
    return redirect('cart')

@require_POST
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('cart')

@require_POST
def clear_cart(request):
    request.session['cart'] = {}
    return redirect('cart')

# Обновленный view корзины
def cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id, is_deleted=False)
            item_total = product.price * quantity
            cart_items.append({
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'quantity': quantity,
                'image': product.image.url if product.image else None,
                'item_total': item_total,
            })
            total += item_total
        except Product.DoesNotExist:
            continue
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

def order(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart')
    from .models import Product, Order, OrderPosition
    cart_items = []
    total = 0
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id, is_deleted=False)
            item_total = product.price * quantity
            cart_items.append({
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'quantity': quantity,
                'item_total': item_total,
            })
            total += item_total
        except Product.DoesNotExist:
            continue
    delivery_price = 300
    total_with_delivery = total + delivery_price
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        if name and address and phone:
            order = Order.objects.create(
                order_number=f'ORD-{Order.objects.count()+1:03d}',
                delivery_address=address,
                phone_number=phone,
                customer_name=name,
            )
            for item in cart_items:
                OrderPosition.objects.create(
                    order=order,
                    product_id=item['id'],
                    quantity=item['quantity'],
                )
            request.session['cart'] = {}
            return render(request, 'eshop/order_success.html', {'order': order})
        else:
            error = 'Пожалуйста, заполните все поля.'
            return render(request, 'eshop/order.html', {'cart_items': cart_items, 'total': total, 'delivery': delivery_price, 'total_with_delivery': total_with_delivery, 'error': error})
    return render(request, 'eshop/order.html', {'cart_items': cart_items, 'total': total, 'delivery': delivery_price, 'total_with_delivery': total_with_delivery})

# Ограничение доступа к подтвержденным заказам (пример)
@user_passes_test(lambda u: u.is_superuser)
def confirmed_orders(request):
    orders = Order.objects.all()
    return render(request, 'eshop/confirmed_orders.html', {'orders': orders})

def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return render(request, 'eshop/register_done.html', {'new_user': new_user})
    else:
        form = UserRegistrationForm()
    return render(request, 'eshop/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'eshop/login.html', {'form': form, 'error': 'Неверный логин или пароль'})
    else:
        form = UserLoginForm()
    return render(request, 'eshop/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')
