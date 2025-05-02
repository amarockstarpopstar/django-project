from django.core.management.base import BaseCommand
from django.utils import timezone
from eshop.models import Category, Tag, Product, Order, OrderPosition
import random
from decimal import Decimal

class Command(BaseCommand):
    help = 'Populates the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating database...')
        
        # Create categories
        self.stdout.write('Creating categories...')
        categories = [
            {'name': 'Электроника', 'description': 'Электронные устройства и гаджеты'},
            {'name': 'Одежда', 'description': 'Мужская и женская одежда различных стилей'},
            {'name': 'Книги', 'description': 'Художественная и научная литература'},
        ]
        
        category_objects = []
        for category in categories:
            category_obj, created = Category.objects.get_or_create(
                name=category['name'],
                defaults={'description': category['description']}
            )
            category_objects.append(category_obj)
            self.stdout.write(f'- {"Created" if created else "Found"} category: {category_obj.name}')
        
        # Create tags
        self.stdout.write('Creating tags...')
        tags = [
            {'name': 'Новинка', 'description': 'Недавно добавленные товары'},
            {'name': 'Хит продаж', 'description': 'Популярные товары'},
            {'name': 'Скидка', 'description': 'Товары со скидкой'},
            {'name': 'Рекомендуем', 'description': 'Рекомендуемые товары'},
            {'name': 'Акция', 'description': 'Товары, участвующие в акции'},
        ]
        
        tag_objects = []
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                name=tag['name'],
                defaults={'description': tag['description']}
            )
            tag_objects.append(tag_obj)
            self.stdout.write(f'- {"Created" if created else "Found"} tag: {tag_obj.name}')
        
        # Create products
        self.stdout.write('Creating products...')
        products = [
            {
                'name': 'Смартфон Samsung Galaxy S21',
                'description': 'Современный смартфон с отличной камерой и высокой производительностью',
                'price': Decimal('49999.99'),
                'category': category_objects[0],  # Электроника
            },
            {
                'name': 'Ноутбук Apple MacBook Pro',
                'description': 'Мощный ноутбук для работы и творчества',
                'price': Decimal('129999.99'),
                'category': category_objects[0],  # Электроника
            },
            {
                'name': 'Футболка хлопковая',
                'description': 'Удобная хлопковая футболка для повседневной носки',
                'price': Decimal('1999.99'),
                'category': category_objects[1],  # Одежда
            },
            {
                'name': 'Джинсы классические',
                'description': 'Классические джинсы прямого кроя',
                'price': Decimal('3999.99'),
                'category': category_objects[1],  # Одежда
            },
            {
                'name': 'Роман "Мастер и Маргарита"',
                'description': 'Известный роман Михаила Булгакова',
                'price': Decimal('799.99'),
                'category': category_objects[2],  # Книги
            },
            {
                'name': 'Сборник "100 лучших стихотворений"',
                'description': 'Коллекция лучших стихотворений классиков',
                'price': Decimal('899.99'),
                'category': category_objects[2],  # Книги
            },
        ]
        
        product_objects = []
        for product in products:
            product_obj, created = Product.objects.get_or_create(
                name=product['name'],
                defaults={
                    'description': product['description'],
                    'price': product['price'],
                    'category': product['category'],
                    'is_deleted': False
                }
            )
            
            # Add random tags to products
            if created:
                random_tags = random.sample(tag_objects, random.randint(1, 3))
                for tag in random_tags:
                    product_obj.tags.add(tag)
            
            product_objects.append(product_obj)
            self.stdout.write(f'- {"Created" if created else "Found"} product: {product_obj.name}')
        
        # Create orders
        self.stdout.write('Creating orders...')
        orders = [
            {
                'order_number': 'ORD-001',
                'delivery_address': 'ул. Ленина, д. 10, кв. 25, г. Москва',
                'phone_number': '+7 (916) 123-45-67',
                'customer_name': 'Иванов Иван Иванович',
            },
            {
                'order_number': 'ORD-002',
                'delivery_address': 'ул. Пушкина, д. 5, кв. 12, г. Санкт-Петербург',
                'phone_number': '+7 (905) 987-65-43',
                'customer_name': 'Петрова Анна Сергеевна',
            },
            {
                'order_number': 'ORD-003',
                'delivery_address': 'ул. Гагарина, д. 15, кв. 45, г. Новосибирск',
                'phone_number': '+7 (912) 555-55-55',
                'customer_name': 'Сидоров Алексей Петрович',
            },
        ]
        
        order_objects = []
        for order_data in orders:
            order_obj, created = Order.objects.get_or_create(
                order_number=order_data['order_number'],
                defaults={
                    'delivery_address': order_data['delivery_address'],
                    'phone_number': order_data['phone_number'],
                    'customer_name': order_data['customer_name'],
                }
            )
            order_objects.append(order_obj)
            self.stdout.write(f'- {"Created" if created else "Found"} order: {order_obj.order_number}')
        
        # Create order positions
        self.stdout.write('Creating order positions...')
        positions = []
        for i, order in enumerate(order_objects):
            # Each order will have 2-3 positions
            num_positions = random.randint(2, 3)
            selected_products = random.sample(product_objects, num_positions)
            
            for product in selected_products:
                quantity = random.randint(1, 5)
                discount = Decimal(random.randint(0, 15)) / 100  # 0-15% discount
                
                position, created = OrderPosition.objects.get_or_create(
                    order=order,
                    product=product,
                    defaults={
                        'quantity': quantity,
                        'discount': discount * product.price,
                    }
                )
                positions.append(position)
                self.stdout.write(f'- {"Created" if created else "Found"} position: {product.name} in order {order.order_number}')
        
        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))
        self.stdout.write(f'Created {len(category_objects)} categories, {len(tag_objects)} tags, {len(product_objects)} products, {len(order_objects)} orders, and {len(positions)} order positions.') 