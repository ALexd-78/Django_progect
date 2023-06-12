from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from catalog.models import Product, Blog


class ProductListView(generic.ListView):
    '''контроллер домашней страницы'''
    model = Product
    extra_context = {
        'title': 'Главная'
    }


class ProductDetailView(generic.DetailView):
    '''контроллер постраничного вывода информации о продукте'''
    model = Product

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = context_data['object']
        return context_data


class BlogListView(generic.ListView):
    '''контроллер страницы со статьями'''
    model = Blog
    extra_context = {
        'title': 'Статьи'
    }


    def get_queryset(self):
        '''вывод с фильтрацией'''
        queryset = super().get_queryset()
        queryset = queryset.filter(is_publication=True)
        return queryset


class BlogDetailView(generic.DetailView):
    '''контроллер постраничного вывода информации о статье'''
    model = Blog

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = context_data['blog']
        return context_data

    def get_object(self, queryset=None):
        '''счётчик просмотров'''
        item = super().get_object(queryset)
        item.count_views += 1
        item.save()
        return item


class BlogCreateView(generic.CreateView):
    model = Blog
    fields = ('heading', 'content', 'preview', )
    success_url = reverse_lazy('catalog:blog_list')


class BlogUpdateView(generic.UpdateView):
    model = Blog
    fields = ('heading', 'slug', 'content', 'preview', )

    def get_success_url(self):
        return reverse('catalog:blog_item', kwargs={'pk': self.object.pk})
    # success_url = reverse_lazy('catalog:blog_item')


class BlogDeleteView(generic.DeleteView):
    model = Blog
    success_url = reverse_lazy('catalog:blog_list')


def toggle_publication(request, pk):
    blog_item = get_object_or_404(Blog, pk=pk)
    if blog_item.is_publication:
        blog_item.is_publication = False
    else:
        blog_item.is_publication = True
    blog_item.save()
    return redirect(reverse('catalog:blog_update', args=[blog_item.pk]))

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
