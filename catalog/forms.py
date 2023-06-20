from  django import forms

from catalog.models import Product, Blog, Version

valid_works = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']


class FormStyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProductForm(FormStyleMixin, forms.ModelForm):

    class Meta:
        model = Product
        # fields = '__all__'
        # fields = ('name', 'description', 'category', 'unit_price',)
        exclude = ('is_publicate',)

    def clean_name(self):
        cleaned_data = self.cleaned_data['name']
        for word in valid_works:
            if word in cleaned_data:
                raise forms.ValidationError(f'Слово {word} недопустимо для применения в этом пункте')
        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data['description']
        for word in valid_works:
            if word in cleaned_data:
                raise forms.ValidationError(f'Слово {word} недопустимо для применения в этом пункте')
        return cleaned_data



class BlogForm(FormStyleMixin, forms.ModelForm):

    class Meta:
        model =Blog
        # fields = '__all__'
        # fields = ('name', 'description', 'category', 'unit_price',)
        exclude = ('is_publication',)


class VersionForm(FormStyleMixin, forms.ModelForm):

    class Meta:
        model = Version
        fields = '__all__'