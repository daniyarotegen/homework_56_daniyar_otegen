from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect, get_object_or_404
from market.forms import ProductForm, ProductSearchForm
from market.models import Product, CategoryChoice


def index_view(request: WSGIRequest):
    form = ProductSearchForm(request.GET)
    categories = []
    for category_value, category_label in CategoryChoice.choices:
        products_in_category = Product.objects.filter(category=category_value, quantity__gt=0)
        if products_in_category.exists():
            categories.append((category_value, category_label))
    if form.is_valid():
        name = form.cleaned_data.get('name')
        products = Product.objects.filter(name__icontains=name, quantity__gt=0).order_by('name')
    else:
        products = Product.objects.filter(quantity__gt=0).order_by('name')

    context = {
        'products': products,
        'form': form,
        'categories': categories
    }

    return render(request, 'index.html', context=context)


def category_view(request: WSGIRequest, category_code):
    form = ProductSearchForm(request.GET)

    if form.is_valid():
        name = form.cleaned_data.get('name')
        products = Product.objects.filter(category=category_code, name__icontains=name, quantity__gt=0).order_by('name')
    else:
        products = Product.objects.filter(category=category_code, quantity__gt=0).order_by('name')

    category_name = ''
    for category_value, category_label in CategoryChoice.choices:
        if category_value == category_code:
            category_name = category_label

    context = {
        'products': products,
        'form': form,
        'category_code': category_code,
        'category_name': category_name,
        'categories': CategoryChoice.choices
    }
    return render(request, 'products_by_category.html', context=context)


def add_view(request: WSGIRequest):
    if request.method == 'GET':
        form = ProductForm()
        return render(request, 'product_create.html', {'form': form})
    form = ProductForm(data=request.POST)
    if not form.is_valid():
        return render(request, 'product_create.html', context={
            'form': form
        })
    else:
        product = Product.objects.create(**form.cleaned_data)
        return redirect('product_detail', pk=product.pk)


def detailed_view(request: WSGIRequest, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', context={'product': product, 'categories': CategoryChoice.choices})


def update_view(request: WSGIRequest, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product.name = form.clean_name()
            product.description = form.cleaned_data['description']
            product.image = form.cleaned_data['image']
            product.category = form.cleaned_data['category']
            product.quantity = form.cleaned_data['quantity']
            product.price = form.cleaned_data['price']
            product.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(initial={
            'name': product.name,
            'description': product.description,
            'image': product.image,
            'category': product.category,
            'quantity': product.quantity,
            'price': product.price
        })
    return render(request, 'product_update.html', {'form': form, 'product': product})


def delete_view(request: WSGIRequest, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('index')
    context = {
        'product': product,
    }
    return render(request, 'product_delete.html', context)
