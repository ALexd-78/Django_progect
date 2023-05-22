from django.shortcuts import render

from catalog.models import Product


# def index(request):
#     context = {
#         'product_list': Product.objects.all()
#     }
#     return render(request, 'catalog/index.html', context)


def home(request):
    '''контроллер домашней страницы'''
    context = {
            'product_list': Product.objects.all()
        }
    return render(request, 'catalog/home.html', context)


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


def product(request, pk):
    '''контроллер постраничного вывода информации о продукте'''
    product_item = Product.objects.get(pk=pk)
    context = {
        'object': product_item,
        'title': product_item
    }
    return render(request, 'catalog/product.html', context)