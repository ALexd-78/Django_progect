from django.shortcuts import render

def get_home(request):
    '''контроллер домашней страницы'''
    return render(request, 'catalog/home.html')


def get_contacts(request):
    '''контроллер контактов'''
    if request.method == 'POST':
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message', '')
        print(f'User {name} with phone {phone} send message: {message}')
    return render(request, 'catalog/contacts.html')


