from django.contrib import admin

from catalog.models import Product, Category, Blog, Version

# admin.site.register(Product)
# admin.site.register(Category)
# admin.site.register(Blog)
# admin.site.register(Version)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'unit_price', 'category')
    search_fields = ('name', 'description')
    list_filter = ('category',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'heading', 'slug', 'create_date', 'count_views')
    search_fields = ('heading', 'slug')
    list_filter = ('is_publication', 'create_date', 'count_views')
    prepopulated_fields = {'slug': ('heading',)}


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'number', 'is_active')
    search_fields = ('product', 'name', 'number',)
    list_filter = ('name', 'is_active')