import json

from django.core.management import BaseCommand, call_command

from catalog.models import Category, Product


class Command(BaseCommand):

    def handle(self, *args, **options):

        # удаление данных из таблицы Category
        Category.objects.all().delete()
        # удаление данных из таблицы Product
        Product.objects.all().delete()

        # наполнение таблицы Category из json-файла
        call_command('loaddata', 'catalog_category.json')
        # наполнение таблицы Product из json-файла
        call_command('loaddata', 'catalog_product.json')

        # наполнение таблицы Category из json-файла
        # with open('catalog_category.json', 'r', encoding='UTF8') as file:
        #     data = json.load(file)
        #     data_category = []
        #     for i in data:
        #         data_category.append(Category(id))
        #         data_category.append(Category(i['fields']['name']))
        #         data_category.append(Category(i['fields']['description']))
        #
        # Category.objects.bulk_create(data_category)

        # # наполнение таблицы Product из json-файла
        # with open('catalog_product.json', 'r', encoding='UTF8') as file:
        #     data = json.load(file)
        #     data_product = []
        #     for i in data:
        #         if 'category' in i:
        #             category = Category.objects.get(pk=int(i['category']))
        #         data_product.append(Product(**i['fields']))
        #
        # Product.objects.bulk_create(data_product)
        #
