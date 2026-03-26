from .models import Category, Product
from django.db.models import F


def product_list(request):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    return {
        'category': category,
        'categories': categories,
        'products': products,
        'construction_goods': Product.objects.filter(
            category__slug='construction-materials',
            available=True
        ).order_by('-created')[:5],

        'all_construction_goods': Product.objects.filter(
            category__slug='construction-materials',
            available=True
        ).order_by('-created')[:5],

        'natural_stones': Product.objects.filter(
            category__slug='natural-stones',
            available=True
        ).order_by('-created')[:5],

        'all_natural_stones': Product.objects.filter(
            category__slug='natural-stones',
            available=True
        ).order_by('-created'),

       'discounted_products': Product.objects.filter(
        available=True,
        old_price__isnull=False,
        old_price__gt=F('price')
        ).order_by('-created')[:4],

        'top_products': Product.objects.filter(
            available=True,
            old_price__isnull=False,
            old_price__gt=F('price')
        ).order_by('-created')[:5],

    }