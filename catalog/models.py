from django.db import models

NULLABLE = {'blank': True, 'null': True}

class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='products/', verbose_name='Изображение', **NULLABLE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    unit_price = models.IntegerField(verbose_name='Цена за покупку')
    creation_date = models.DateField(verbose_name='Дата создания')
    modified_date = models.DateField(verbose_name='Дата последнего изменения')

    def __str__(self):
        return f'{self.name}, {self.unit_price}, {self.category}'

    class Meta:
        '''Класс мета-настроек'''
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ('name',)  # сортировка, '-name' - сортировка в обратном порядке


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        '''Класс мета-настроек'''
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('name',)  # сортировка, '-name' - сортировка в обратном порядке


class Blog(models.Model):
    heading = models.CharField(max_length=150, verbose_name='Заголовок')
    slug = models.CharField(max_length=150, verbose_name='Слаг', **NULLABLE)
    content = models.TextField(verbose_name='Содержимое')
    preview = models.ImageField(upload_to='blogs/', verbose_name='Изображение', **NULLABLE)
    create_date = models.DateField(verbose_name='Дата создания')
    is_publication = models.BooleanField(default=True, verbose_name='Опубликовано')
    count_views = models.IntegerField(default=0, verbose_name='Количество просмотров')

    def __str__(self):
        return f'{self.heading}'

    def delete(self, *args, **kwargs):
        self.is_publication = False
        self.save()

    class Meta:
        '''Класс мета-настроек'''
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ('heading',)