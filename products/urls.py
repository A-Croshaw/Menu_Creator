from django.urls import path
from . import views

urlpatterns = [
    path('', views.products_home, name='products'),
    path('all/', views.all_products, name='products_all'),
]
