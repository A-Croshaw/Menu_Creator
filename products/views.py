from django.shortcuts import get_object_or_404, redirect, reverse, render
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Product, Category, Subcategory

def products_home(request):
    """
    A view to render products manager
    """
    return render(request, 'products/products_home.html')

def all_products(request):
    """
    A view to render all products with sorting and searching
    """
    products = Product.objects.all()
    categories = None
    query = None
    sort = None
    direction = None
    subcategories = None

    if request.GET:

        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__category'
            if sortkey == 'subcategory':
                sortkey = 'subcategory__category'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__category__in=categories)
            categories = Category.objects.filter(category__in=categories)

        if 'subcategory' in request.GET:
            subcategories = request.GET['subcategory'].split(',')
            products = products.filter(subcategory__subcategory__in=subcategories)
            subcategories = Subcategory.objects.filter(subcategory__in=subcategories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "No products with that criteria")
                return redirect(reverse('products_all'))

            queries = Q(name__icontains=query)
            products = products.filter(queries)

    current_sorted = f'{sort}_{direction}'
    context = {
        'products': products,
        'search_term': query,
        'sorted_categories': categories,
        'sorted_subcategories': subcategories,
        'current_sorted': current_sorted
    }

    return render(request, 'products/products_all.html', context)