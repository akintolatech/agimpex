import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from cart.forms import CartAddProductForm
from .favourites import Favorites
from .models import Category, Product


def toggle_favorite(request, product_id):
    if request.method != "POST":
        return JsonResponse({'error': 'Invalid request'}, status=400)

    product = get_object_or_404(Product, id=product_id, available=True)

    favorites = Favorites(request)
    is_favorite = favorites.toggle(product.id)

    return JsonResponse({
        'status': 'added' if is_favorite else 'removed',
        'is_favorite': is_favorite,
        'favorite_count': len(favorites),
    })


def favorite_list(request):
    favorites = Favorites(request)
    favorite_ids = favorites.get_ids()

    favorite_products = Product.objects.filter(id__in=favorite_ids, available=True)

    context = {
        'favorite_products': favorite_products,
        'favorite_product_ids': favorite_ids,
    }
    return render(request, 'shop/product/favorite_list.html', context)


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    favorites = Favorites(request)
    favorite_product_ids = favorites.get_ids()


    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(
        request,
        'shop/product/list.html',
        {
            'category': category,
            'categories': categories,
            'products': products,
            'favorite_product_ids': favorite_product_ids,
        },
    )


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)

    # Create a list of valid combinations for JS
    # Example: [{"price": 5000, "values": [1, 5, 10]}, ...]
    combinations = []
    for pricing in product.pricing_rows.prefetch_related('property_values'):
        combinations.append({
            'price': str(pricing.price),
            'values': list(pricing.property_values.values_list('id', flat=True))
        })

    cart_product_form = CartAddProductForm()

    return render(
        request,
        'shop/product/detail.html',
        {
            'product': product,
            'cart_product_form': cart_product_form,
            'combinations_json': json.dumps(combinations)  # Pass this to JS
        },
    )


# def product_detail(request, id, slug):
#     product = get_object_or_404(
#         Product, id=id, slug=slug, available=True
#     )
#     cart_product_form = CartAddProductForm()
#     return render(
#         request,
#         'shop/product/detail.html',
#         {'product': product, 'cart_product_form': cart_product_form},
#     )
