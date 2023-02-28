from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect, get_object_or_404
from market.forms import ProductForm, ProductSearchForm
from market.models import Product, CategoryChoice


def index_view(request: WSGIRequest):
    form = ProductSearchForm(request.GET)
    all_categories = [(category.value, category.label) for category in CategoryChoice]
    categories_with_products = []

    for category_value, category_label in all_categories:
        products_in_category = Product.objects.filter(category=category_value, quantity__gt=0)
        if products_in_category.exists():
            categories_with_products.append((category_value, category_label))

    if form.is_valid():
        name = form.cleaned_data.get('name')
        products = Product.objects.filter(name__icontains=name, quantity__gt=0).order_by('name')
    else:
        products = Product.objects.filter(quantity__gt=0).order_by('name')

    context = {
        'products': products,
        'form': form,
        'categories': categories_with_products
    }

    return render(request, 'index.html', context=context)


def category_view(request: WSGIRequest, category_code):
    products = Product.objects.filter(category=category_code).order_by('name')
    categories = [(category.value, category.label) for category in CategoryChoice]
    return render(request, 'products_by_category.html', {
        'products': products, 'category_code': category_code, 'categories': categories
    })


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
    categories = [(category.value, category.label) for category in CategoryChoice]
    return render(request, 'product_detail.html', context={'product': product, 'categories': categories})


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
