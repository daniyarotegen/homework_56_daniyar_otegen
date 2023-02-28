from django.contrib import admin

from market.models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image', 'category', 'quantity', 'price')
    search_fields = ('name', 'category')
    list_filter = ('name', 'category',)
    ordering = ('name',)


admin.site.register(Product, ProductAdmin)
