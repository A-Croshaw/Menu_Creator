from django.urls import path
from . import views

urlpatterns = [
    path('', views.products_home, name='products'),
    path('all/', views.all_products, name='products_all'),
    path('add/', views.add_product, name='product_add'),
    path('edit/<int:product_id>/', views.edit_product, name='product_edit'),
    path('delete/<int:product_id>/', views.product_delete, name='product_delete'),
]
