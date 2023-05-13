import json

from django.core.management import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):

    def handle(self, *args, **options):
        #удаление данных из таблицы Product
        Product.objects.all().delete()

        #наполнение таблицы Product из json-файла
        with open('catalog_product.json', 'r', encoding='UTF8') as file:
            data = json.load(file)
            data_product = []
            for i in data:
                data_product.append(Product(**i['fields']))

        Product.objects.bulk_create(data_product)

        #удаление данных из таблицы Category
        Category.objects.all().delete()

        #наполнение таблицы Product из json-файла
        with open('catalog_category.json', 'r', encoding='UTF8') as file:
            data = json.load(file)
            data_category = []
            for i in data:
                data_category.append(Product(**i['fields']))

        Category.objects.bulk_create(data_category)


