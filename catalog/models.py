from django.db import models
from django.urls import reverse

from catalog.services.utils import unique_slugify

NULLABLE = {'blank': True, 'null': True}

class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='products/', verbose_name='Изображение', **NULLABLE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    unit_price = models.IntegerField(verbose_name='Цена за покупку')
    creation_date = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    modified_date = models.DateField(auto_now=True, verbose_name='Дата последнего изменения')

    is_publicate = models.BooleanField(default=True, verbose_name='Опубликовано', **NULLABLE)


    def __str__(self):
        return f'{self.name}, {self.unit_price}, {self.category}'

    def delete(self, *args, **kwargs):
        self.is_publication = False
        self.save()

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
    slug = models.CharField(max_length=150, verbose_name='Слаг', blank=True, unique=True)
    content = models.TextField(verbose_name='Содержимое')
    preview = models.ImageField(upload_to='blogs/', verbose_name='Изображение', **NULLABLE)
    create_date = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    is_publication = models.BooleanField(default=True, verbose_name='Опубликовано')
    count_views = models.IntegerField(default=0, verbose_name='Количество просмотров')

    def __str__(self):
        return f'{self.heading}'

    def delete(self, *args, **kwargs):
        self.is_publication = False
        self.save()

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при их отсутствии заполнения
        """
        if not self.slug:
            self.slug = unique_slugify(self, self.heading)
        else:
            # del(self.slug)
            self.slug = unique_slugify(self, self.heading)

        return super().save(*args, **kwargs)


    class Meta:
        '''Класс мета-настроек'''
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ('heading',)


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, verbose_name='продукт', null=True)
    number = models.CharField(max_length=50, verbose_name='номер версии')
    name = models.CharField(max_length=150, verbose_name='название версии')
    is_active = models.BooleanField(default=True, verbose_name='текущая версия')

    def __str__(self):
        return f'{self.name} ({self.product})'

    class Meta:
        '''Класс мета-настроек'''
        verbose_name = 'версия'
        verbose_name_plural = 'версии'
        ordering = ('name',)  # сортировка, '-name' - сортировка в обратном порядке
