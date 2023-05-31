from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import ProductListView, contacts, ProductDetailView, BlogListView, BlogDetailView

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('contacts/', contacts, name='contacts'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_item'),
    path('blogs/', BlogListView.as_view(), name='blog_list'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog_item'),
]
