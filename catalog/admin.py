from django.contrib import admin

from catalog.models import Product, Category, Blog

# admin.site.register(Product)
# admin.site.register(Category)
# admin.site.register(Blog)

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