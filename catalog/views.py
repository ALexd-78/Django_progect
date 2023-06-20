from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from catalog.forms import ProductForm, BlogForm, VersionForm
from catalog.models import Product, Blog, Version


class ProductListView(generic.ListView):
    '''контроллер домашней страницы'''
    model = Product
    extra_context = {
        'title': 'Главная'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related('version_set')
        return queryset


class ProductDetailView(generic.DetailView):
    '''контроллер постраничного вывода информации о продукте'''
    model = Product

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = context_data['object']
        return context_data


class ProductCreateView(generic.CreateView):
    '''контроллер создания продукта'''
    model = Product
    form_class = ProductForm
    # fields = ('name', 'description', 'category', 'unit_price',)
    success_url = reverse_lazy('catalog:product_list')


class ProductUpdateView(generic.UpdateView):
    '''контроллер изменения продукта'''
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form_with_formset.html'
    # fields = ('name', 'description', 'category', 'unit_price',)
    success_url = reverse_lazy('catalog:product_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset =  inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)



class ProductDeleteView(generic.DeleteView):
    '''контроллер удаления продукта'''
    model = Product
    success_url = reverse_lazy('catalog:product_list')


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
    '''контроллер создания статьи'''
    model = Blog
    form_class = BlogForm
    # fields = ('heading', 'content', 'preview', )
    success_url = reverse_lazy('catalog:blog_list')


class BlogUpdateView(generic.UpdateView):
    '''контроллер редактирования статьи'''
    model = Blog
    form_class = BlogForm
    # fields = ('heading', 'slug', 'content', 'preview', )

    def get_success_url(self):
        return reverse('catalog:blog_item', kwargs={'pk': self.object.pk})
    # success_url = reverse_lazy('catalog:blog_item')


class BlogDeleteView(generic.DeleteView):
    '''контроллер удаления статьи'''
    model = Blog
    success_url = reverse_lazy('catalog:blog_list')


def toggle_publication(request, pk):
    '''контроллер вывода статьи с фильтрацией'''
    blog_item = get_object_or_404(Blog, pk=pk)
    if blog_item.is_publication:
        blog_item.is_publication = False
    else:
        blog_item.is_publication = True
    blog_item.save()
    return redirect(reverse('catalog:blog_update', args=[blog_item.pk]))

def toggle_publicate(request, pk):
    '''контроллер вывода продукта с фильтрацией'''
    product_item = get_object_or_404(Product, pk=pk)
    if product_item.is_publicate:
        product_item.is_publicate = False
    else:
        product_item.is_publicate = True
    product_item.save()
    return redirect(reverse('catalog:product_update', args=[product_item.pk]))

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
