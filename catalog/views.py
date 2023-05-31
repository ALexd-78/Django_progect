from django.shortcuts import render
from django.views import generic

from catalog.models import Product, Blog


class ProductListView(generic.ListView):
    '''контроллер домашней страницы'''
    model = Product


class ProductDetailView(generic.DetailView):
    '''контроллер постраничного вывода информации о продукте'''
    model = Product

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = context_data['object']
        return context_data


def contacts(request):
    '''контроллер контактов'''
    if request.method == 'POST':
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message', '')
        print(f'User {name} with phone {phone} send message: {message}')

    context = {
        'title': 'Контакты'
    }

    return render(request, 'catalog/contacts.html', context)


class BlogListView(generic.ListView):
    '''контроллер страницы со статьями'''
    model = Blog


class BlogDetailView(generic.DetailView):
    '''контроллер постраничного вывода информации о статье'''
    model = Blog

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = context_data['blog']
        return context_data