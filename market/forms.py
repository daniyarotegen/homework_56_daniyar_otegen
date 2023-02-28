from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets
from market.models import Product


class ProductForm(forms.Form):
    CATEGORY_CHOICES = (
        ('CPU', 'Processor'),
        ('GPU', 'Graphics Card'),
        ('MONITOR', 'Monitor'),
        ('MOTHERBOARD', 'Motherboard'),
        ('OTHER', 'Other')
    )
    name = forms.CharField(max_length=100, required=True, label='Name')
    description = forms.CharField(max_length=3000, required=False, label='Details', widget=widgets.Textarea)
    image = forms.URLField(required=False, label='Image URL')
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=True, initial='OTHER', label='Category', )
    quantity = forms.IntegerField(min_value=0, required=True, label='Quantity')
    price = forms.DecimalField(min_value=0, max_digits=7, decimal_places=2, required=True, label='Price')

    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'quantity', 'price']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 2:
            raise ValidationError('Name must be longer than 2 symbols')
        return name


class ProductSearchForm(forms.Form):
    name = forms.CharField(max_length=100, required=False, label='Search by name')
