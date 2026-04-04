from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from shop.models import Product
from .cart import Cart


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, available=True)

    quantity = int(request.POST.get('quantity', 1))
    override = request.POST.get('override', 'False') == 'True'

    # Collect selected property value IDs from fields like property_1, property_2...
    selected_value_ids = []
    for key, value in request.POST.items():
        if key.startswith('property_') and value:
            selected_value_ids.append(value)

    cart.add(
        product=product,
        quantity=quantity,
        override_quantity=override,
        selected_value_ids=selected_value_ids
    )

    return redirect('cart:cart_detail')


@require_POST
def cart_increment(request, cart_key):
    cart = Cart(request)
    cart.increment(cart_key)
    return redirect('cart:cart_detail')


@require_POST
def cart_decrement(request, cart_key):
    cart = Cart(request)
    cart.decrement(cart_key)
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, cart_key):
    cart = Cart(request)
    cart.remove(cart_key)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})




# from django.shortcuts import get_object_or_404, redirect, render
# from django.views.decorators.http import require_POST
#
# from shop.models import Product
# from .cart import Cart
#
#
# @require_POST
# def cart_add(request, product_id):
#     # Get the Cart from session request
#     cart = Cart(request)
#     product = get_object_or_404(Product, id=product_id, available=True)
#
#     quantity = int(request.POST.get('quantity', 1))
#     override = request.POST.get('override', 'False') == 'True'
#
#     # Collect selected property value IDs from fields like property_1, property_2...
#     selected_value_ids = []
#     for key, value in request.POST.items():
#         if key.startswith('property_') and value:
#             selected_value_ids.append(value)
#
#     cart.add(
#         product=product,
#         quantity=quantity,
#         override_quantity=override,
#         selected_value_ids=selected_value_ids
#     )
#
#     return redirect('cart:cart_detail')
#
#
# def cart_remove(request, cart_key):
#     cart = Cart(request)
#     cart.remove(cart_key)
#     return redirect('cart:cart_detail')
#
#
# def cart_detail(request):
#     cart = Cart(request)
#     return render(request, 'cart/detail.html', {'cart': cart})
#



# from django.http import JsonResponse
# from django.shortcuts import get_object_or_404, redirect, render
# from django.views.decorators.http import require_POST
# from shop.models import Product
#
# from .cart import Cart
# from .forms import CartAddProductForm
#
#
# @require_POST
# def cart_add(request, product_id):
#     cart = Cart(request)
#     product = get_object_or_404(Product, id=product_id)
#     form = CartAddProductForm(request.POST)
#     if form.is_valid():
#         cd = form.cleaned_data
#         cart.add(
#             product=product,
#             quantity=cd['quantity'],
#             override_quantity=cd['override'],
#         )
#     return redirect('cart:cart_detail')
#
#
# @require_POST
# def cart_remove(request, product_id):
#     cart = Cart(request)
#     product = get_object_or_404(Product, id=product_id)
#     cart.remove(product)
#     return redirect('cart:cart_detail')
#
#
# def cart_detail(request):
#     cart = Cart(request)
#     for item in cart:
#         item['update_quantity_form'] = CartAddProductForm(
#             initial={'quantity': item['quantity'], 'override': True}
#         )
#     return render(request, 'cart/detail.html', {'cart': cart})