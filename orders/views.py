from django.shortcuts import render
from cart.cart import Cart
from .forms import OrderCreateForm
from .models import OrderItem, OrderItemPropertyValue


def order_create(request):
    cart = Cart(request)

    if len(cart) == 0:
        form = OrderCreateForm()
        return render(
            request,
            'orders/order/create.html',
            {'cart': cart, 'form': form}
        )

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save()

            for item in cart:
                order_item = OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],   # final unit price including adjustments
                    quantity=item['quantity'],
                )

                for prop in item.get('selected_properties', []):
                    OrderItemPropertyValue.objects.create(
                        order_item=order_item,
                        product_property=prop['property_name'],
                        property_value=prop['value_name'],
                        price_adjustment=prop['price_adjustment'],
                    )

            # clear cart after successful order creation
            cart.clear()

            return render(
                request,
                'orders/order/created.html',
                {'order': order}
            )
    else:
        form = OrderCreateForm()

    return render(
        request,
        'orders/order/create.html',
        {'cart': cart, 'form': form},
    )