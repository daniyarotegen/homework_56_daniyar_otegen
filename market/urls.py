from django.urls import path
from market.views import index_view, add_view, detailed_view, update_view, delete_view, category_view

urlpatterns = [
    path("", index_view, name='index'),
    path('product/add/', add_view, name='product_add'),
    path('product/<int:pk>', detailed_view, name='product_detail'),
    path('product/<int:pk>/edit/', update_view, name='product_update'),
    path('product/<int:pk>/delete/', delete_view, name='product_delete'),
    path('products/<str:category_code>/', category_view, name='products_by_category'),
]