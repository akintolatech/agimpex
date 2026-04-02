from decimal import Decimal
from shop.models import Product, ProductPropertyValue


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')

        if not cart:
            cart = self.session['cart'] = {}

        self.cart = cart

    def _generate_key(self, product_id, selected_value_ids):
        """
        Unique cart key for same product with different selected properties.
        Example:
            product 5 + values [2, 9] => "5-2_9"
        """
        selected_value_ids = [int(v) for v in selected_value_ids if v]
        selected_value_ids.sort()

        if selected_value_ids:
            return f"{product_id}-{'_'.join(map(str, selected_value_ids))}"
        return str(product_id)

    def _get_valid_property_values(self, product, selected_value_ids):
        """
        Ensure selected values belong ONLY to the current product.
        """
        selected_value_ids = [int(v) for v in selected_value_ids if v]

        property_values = ProductPropertyValue.objects.filter(
            id__in=selected_value_ids,
            product_property__product=product
        ).select_related('product_property')

        return list(property_values)

    def add(self, product, quantity=1, override_quantity=False, selected_value_ids=None):
        selected_value_ids = selected_value_ids or []
        property_values = self._get_valid_property_values(product, selected_value_ids)

        valid_selected_ids = [value.id for value in property_values]
        cart_key = self._generate_key(product.id, valid_selected_ids)

        total_adjustment = sum(
            (Decimal(str(value.price_adjustment)) for value in property_values),
            Decimal('0.00')
        )

        final_unit_price = product.price + total_adjustment

        selected_properties = [
            {
                'property_id': value.product_property.id,
                'property_name': value.product_property.name,
                'value_id': value.id,
                'value_name': value.value,
                'price_adjustment': str(value.price_adjustment),
            }
            for value in property_values
        ]

        if cart_key not in self.cart:
            self.cart[cart_key] = {
                'product_id': product.id,
                'quantity': 0,
                'price': str(final_unit_price),      # final unit price
                'base_price': str(product.price),    # original product price
                'selected_properties': selected_properties,
            }

        if override_quantity:
            self.cart[cart_key]['quantity'] = quantity
        else:
            self.cart[cart_key]['quantity'] += quantity

        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, cart_key):
        if cart_key in self.cart:
            del self.cart[cart_key]
            self.save()

    def update(self, cart_key, quantity):
        if cart_key in self.cart:
            if quantity > 0:
                self.cart[cart_key]['quantity'] = quantity
            else:
                del self.cart[cart_key]
            self.save()

    def __iter__(self):
        product_ids = [item['product_id'] for item in self.cart.values()]
        products = Product.objects.filter(id__in=product_ids)
        products_map = {product.id: product for product in products}

        for cart_key, item in self.cart.items():
            cart_item = item.copy()
            cart_item['cart_key'] = cart_key
            cart_item['product'] = products_map.get(item['product_id'])
            cart_item['price'] = Decimal(item['price'])
            cart_item['base_price'] = Decimal(item['base_price'])
            cart_item['total_price'] = cart_item['price'] * cart_item['quantity']
            yield cart_item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(
            (Decimal(item['price']) * item['quantity'] for item in self.cart.values()),
            Decimal('0.00')
        )

    def clear(self):
        if 'cart' in self.session:
            del self.session['cart']
            self.save()

# from decimal import Decimal
#
# from django.conf import settings
# from shop.models import Product
#
#
# class Cart:
#     def __init__(self, request):
#         """
#         Initialize the cart.
#         """
#         self.session = request.session
#         cart = self.session.get(settings.CART_SESSION_ID)
#
#         if not cart:
#             # Save an empty cart in the session
#             cart = self.session[settings.CART_SESSION_ID] = {}
#
#         self.cart = cart
#
#     def __iter__(self):
#         """
#         Iterate over the items in the cart and fetch the products
#         from the database. Skip products that no longer exist.
#         """
#         product_ids = self.cart.keys()
#
#         # Get the product objects and add them to the cart
#         products = Product.objects.filter(id__in=product_ids)
#         cart = self.cart.copy()
#
#         for product in products:
#             cart[str(product.id)]['product'] = product
#
#         for item in cart.values():
#
#             if 'product' not in item:
#                 continue
#
#             item['price'] = Decimal(item['price'])
#             item['total_price'] = item['price'] * item['quantity']
#             yield item
#
#     def __len__(self):
#         """
#         Count all quantities in the cart.
#         """
#         return sum(item['quantity'] for item in self.cart.values())
#
#     def add(self, product, quantity=1, override_quantity=False):
#         """
#         Add a product to the cart or update its quantity.
#         """
#         product_id = str(product.id)
#
#         if product_id not in self.cart:
#             self.cart[product_id] = {
#                 'quantity': 0,
#                 'price': str(product.price),
#             }
#
#         if override_quantity:
#             self.cart[product_id]['quantity'] = quantity
#         else:
#             self.cart[product_id]['quantity'] += quantity
#
#         self.save()
#
#     def save(self):
#         """
#         Mark the session as modified to make sure it gets saved.
#         """
#         self.session.modified = True
#
#     def remove(self, product):
#         """
#         Remove a product from the cart.
#         """
#         product_id = str(product.id)
#
#         if product_id in self.cart:
#             del self.cart[product_id]
#             self.save()
#
#     def clear(self):
#         """
#         Remove cart from session.
#         """
#         if settings.CART_SESSION_ID in self.session:
#             del self.session[settings.CART_SESSION_ID]
#             self.save()
#
#     def get_total_price(self):
#         """
#         Return the total cost of existing products only.
#         This avoids counting deleted products still stored in session.
#         """
#         total = Decimal('0')
#         product_ids = self.cart.keys()
#         products = Product.objects.filter(id__in=product_ids)
#
#         for product in products:
#             item = self.cart.get(str(product.id))
#             if item:
#                 total += Decimal(item['price']) * item['quantity']
#
#         return total