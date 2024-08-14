from django.contrib.auth.decorators import (
    login_required, permission_required)
from django.shortcuts import get_object_or_404, redirect, reverse, render
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Product, Category, Subcategory
from .forms import ProductForm

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
                sortkey = 'subcategory__subcategory'
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


@login_required
@permission_required("products.product_add", raise_exception=True)
def add_product(request):
    """ Adding products, (admin users only) """
    if not request.user.is_superuser:
        messages.error(request, 'Admin users can only add products.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'{product.name} was successfully added')
            return redirect(reverse('products_all'))
        else:
            messages.error(request,
                           f'failed to add {product.name}.'
                           'Please ensure the details are correct and'
                           'all fields that are required are entered.'
                           )
    else:
        form = ProductForm()

    template = 'products/product_add.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


@login_required
@permission_required("products.product_edit", raise_exception=True)
def edit_product(request, product_id):
    """ Edit a product """
    if not request.user.is_superuser:
        messages.error(request, 'Admin users only can edit products.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'{product.name} was successfully updated!')
            return redirect(reverse('products'))
        else:
            messages.error(
                request,
                f'Updating {product.name} failed.'
                ' Please ensure the details are valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'Editing: {product.name}')

    template = 'products/product_edit.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
@permission_required("products.product_delete", raise_exception=True)
def product_delete(request, product_id):
    """ Delete product """
    if not request.user.is_superuser:
        messages.error(request, 'Admin users can only delete products.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == "POST":
        product.delete()
        messages.success(
            request, f'{product.name} has been delete successfully!')
        return redirect(reverse('products'))

    context = {
        'product': product,
    }
    return render(request, "products/product_delete.html", context)
