from django.urls import path

from catalog.apps import CatalogConfig
# from catalog.views import index

from catalog.views import home, contacts


app_name = CatalogConfig.name

urlpatterns = [
    # path('', index),
    path('', home),
    path('contacts/', contacts),

]

