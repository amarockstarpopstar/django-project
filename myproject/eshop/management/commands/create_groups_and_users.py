from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from eshop.models import Product, Category, Tag

class Command(BaseCommand):
    help = 'Создает 10 пользователей и группы с нужными правами доступа'

    def handle(self, *args, **kwargs):
        # Создание групп
        superuser_group, _ = Group.objects.get_or_create(name='Суперпользователь')
        seller_group, _ = Group.objects.get_or_create(name='Продавец')
        admin_group, _ = Group.objects.get_or_create(name='Администратор')
        buyer_group, _ = Group.objects.get_or_create(name='Покупатель')

        # Получение прав
        add_product = Permission.objects.get(codename='add_product')
        change_product = Permission.objects.get(codename='change_product')
        delete_product = Permission.objects.get(codename='delete_product')
        view_product = Permission.objects.get(codename='view_product')
        add_category = Permission.objects.get(codename='add_category')
        change_category = Permission.objects.get(codename='change_category')
        delete_category = Permission.objects.get(codename='delete_category')
        view_category = Permission.objects.get(codename='view_category')
        add_tag = Permission.objects.get(codename='add_tag')
        change_tag = Permission.objects.get(codename='change_tag')
        delete_tag = Permission.objects.get(codename='delete_tag')
        view_tag = Permission.objects.get(codename='view_tag')

        # Права для продавца
        seller_group.permissions.set([
            add_product, change_product, delete_product, view_product
        ])
        # Права для администратора
        admin_group.permissions.set([
            add_product, change_product, delete_product, view_product,
            add_category, change_category, delete_category, view_category,
            add_tag, change_tag, delete_tag, view_tag
        ])
        # Права для покупателя
        buyer_group.permissions.set([
            view_product, view_category, view_tag
        ])

        # Создание пользователей
        users = [
            ('superuser', 'superuserpass', superuser_group),
            ('seller1', 'sellerpass1', seller_group),
            ('seller2', 'sellerpass2', seller_group),
            ('seller3', 'sellerpass3', seller_group),
            ('admin1', 'adminpass1', admin_group),
            ('admin2', 'adminpass2', admin_group),
            ('buyer1', 'buyerpass1', buyer_group),
            ('buyer2', 'buyerpass2', buyer_group),
            ('buyer3', 'buyerpass3', buyer_group),
            ('buyer4', 'buyerpass4', buyer_group),
        ]
        for username, password, group in users:
            if not User.objects.filter(username=username).exists():
                if username == 'superuser':
                    user = User.objects.create_superuser(username=username, password=password)
                else:
                    user = User.objects.create_user(username=username, password=password)
                user.groups.add(group)
        self.stdout.write(self.style.SUCCESS('Пользователи и группы успешно созданы!'))
