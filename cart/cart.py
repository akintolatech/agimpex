from decimal import Decimal
from django.conf import settings
from shop.models import Product, ProductPropertyValue


class Cart:
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def _generate_key(self, product_id, selected_value_ids):
        """
        Create a unique key for same product with different selected properties.
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
        Ensure selected property values belong to this product only.
        """
        selected_value_ids = [int(v) for v in selected_value_ids if v]

        property_values = ProductPropertyValue.objects.filter(
            id__in=selected_value_ids,
            product_property__product=product
        ).select_related('product_property')

        return list(property_values)

    def add(self, product, quantity=1, override_quantity=False, selected_value_ids=None):
        """
        Add product with selected property values.
        Price is determined from ProductPricing combination if available.
        """
        selected_value_ids = selected_value_ids or []

        # Validate selected values belong to product
        property_values = self._get_valid_property_values(product, selected_value_ids)
        valid_selected_ids = [value.id for value in property_values]

        # Generate unique cart key
        cart_key = self._generate_key(product.id, valid_selected_ids)

        # Determine final price from ProductPricing table
        final_unit_price = product.get_price_for_properties(valid_selected_ids)

        # Fallback to base product price if no matching combination
        if final_unit_price is None:
            final_unit_price = product.price

        # Save selected properties for display in cart
        selected_properties = [
            {
                'property_id': value.product_property.id,
                'property_name': value.product_property.name,
                'value_id': value.id,
                'value_name': value.value,
            }
            for value in property_values
        ]

        if cart_key not in self.cart:
            self.cart[cart_key] = {
                'product_id': product.id,
                'quantity': 0,
                'price': str(final_unit_price),      # final unit price for this combination
                'base_price': str(product.price),    # original base product price
                'selected_properties': selected_properties,
            }

        if override_quantity:
            self.cart[cart_key]['quantity'] = quantity
        else:
            self.cart[cart_key]['quantity'] += quantity

        self.save()

    def save(self):
        """
        Mark session as modified.
        """
        self.session.modified = True

    def remove(self, cart_key):
        """
        Remove item by cart key.
        """
        if cart_key in self.cart:
            del self.cart[cart_key]
            self.save()

    def update(self, cart_key, quantity):
        """
        Update quantity by cart key.
        """
        if cart_key in self.cart:
            if quantity > 0:
                self.cart[cart_key]['quantity'] = quantity
            else:
                del self.cart[cart_key]
            self.save()

    def increment(self, cart_key, amount=1):
        """
        Increase quantity of exact cart item.
        """
        if cart_key in self.cart:
            self.cart[cart_key]['quantity'] += amount
            self.save()

    def decrement(self, cart_key, amount=1):
        """
        Decrease quantity of exact cart item.
        Remove item if quantity becomes 0 or less.
        """
        if cart_key in self.cart:
            self.cart[cart_key]['quantity'] -= amount

            if self.cart[cart_key]['quantity'] <= 0:
                del self.cart[cart_key]

            self.save()

    def get_item(self, cart_key):
        """
        Return raw cart item by cart_key.
        """
        return self.cart.get(cart_key)

    def __iter__(self):
        """
        Iterate through cart items.
        """
        product_ids = [item['product_id'] for item in self.cart.values()]
        products = Product.objects.filter(id__in=product_ids)
        products_map = {product.id: product for product in products}

        for cart_key, item in self.cart.items():
            cart_item = item.copy()
            cart_item['cart_key'] = cart_key
            cart_item['product'] = products_map.get(item['product_id'])

            # Skip if product no longer exists
            if not cart_item['product']:
                continue

            cart_item['price'] = Decimal(item['price'])
            cart_item['base_price'] = Decimal(item.get('base_price', item['price']))
            cart_item['total_price'] = cart_item['price'] * cart_item['quantity']

            yield cart_item

    def __len__(self):
        """
        Count total quantities.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Total price of cart.
        """
        return sum(
            (Decimal(item['price']) * item['quantity'] for item in self.cart.values()),
            Decimal('0.00')
        )

    def clear(self):
        """
        Clear cart.
        """
        if settings.CART_SESSION_ID in self.session:
            del self.session[settings.CART_SESSION_ID]
            self.save()


# from decimal import Decimal
# from django.conf import settings
# from shop.models import Product, ProductPropertyValue
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
#             cart = self.session[settings.CART_SESSION_ID] = {}
#
#         self.cart = cart
#
#     def _generate_key(self, product_id, selected_value_ids):
#         """
#         Create a unique key for same product with different selected properties.
#         Example:
#             product 5 + values [2, 9] => "5-2_9"
#         """
#         selected_value_ids = [int(v) for v in selected_value_ids if v]
#         selected_value_ids.sort()
#
#         if selected_value_ids:
#             return f"{product_id}-{'_'.join(map(str, selected_value_ids))}"
#         return str(product_id)
#
#     def _get_valid_property_values(self, product, selected_value_ids):
#         """
#         Ensure selected property values belong to this product only.
#         """
#         selected_value_ids = [int(v) for v in selected_value_ids if v]
#
#         property_values = ProductPropertyValue.objects.filter(
#             id__in=selected_value_ids,
#             product_property__product=product
#         ).select_related('product_property')
#
#         return list(property_values)
#
#     def add(self, product, quantity=1, override_quantity=False, selected_value_ids=None):
#         """
#         Add product with selected property values.
#         Price is determined from ProductPricing combination if available.
#         """
#         selected_value_ids = selected_value_ids or []
#
#         # Validate selected values belong to product
#         property_values = self._get_valid_property_values(product, selected_value_ids)
#         valid_selected_ids = [value.id for value in property_values]
#
#         # Generate unique cart key
#         cart_key = self._generate_key(product.id, valid_selected_ids)
#
#         # Determine final price from ProductPricing table
#         final_unit_price = product.get_price_for_properties(valid_selected_ids)
#
#         # Fallback to base product price if no matching combination
#         if final_unit_price is None:
#             final_unit_price = product.price
#
#         # Save selected properties for display in cart
#         selected_properties = [
#             {
#                 'property_id': value.product_property.id,
#                 'property_name': value.product_property.name,
#                 'value_id': value.id,
#                 'value_name': value.value,
#             }
#             for value in property_values
#         ]
#
#         if cart_key not in self.cart:
#             self.cart[cart_key] = {
#                 'product_id': product.id,
#                 'quantity': 0,
#                 'price': str(final_unit_price),      # final unit price for this combination
#                 'base_price': str(product.price),    # original base product price
#                 'selected_properties': selected_properties,
#             }
#
#         if override_quantity:
#             self.cart[cart_key]['quantity'] = quantity
#         else:
#             self.cart[cart_key]['quantity'] += quantity
#
#         self.save()
#
#     def save(self):
#         """
#         Mark session as modified.
#         """
#         self.session.modified = True
#
#     def remove(self, cart_key):
#         """
#         Remove item by cart key.
#         """
#         if cart_key in self.cart:
#             del self.cart[cart_key]
#             self.save()
#
#     def update(self, cart_key, quantity):
#         """
#         Update quantity by cart key.
#         """
#         if cart_key in self.cart:
#             if quantity > 0:
#                 self.cart[cart_key]['quantity'] = quantity
#             else:
#                 del self.cart[cart_key]
#             self.save()
#
#     def __iter__(self):
#         """
#         Iterate through cart items.
#         """
#         product_ids = [item['product_id'] for item in self.cart.values()]
#         products = Product.objects.filter(id__in=product_ids)
#         products_map = {product.id: product for product in products}
#
#         for cart_key, item in self.cart.items():
#             cart_item = item.copy()
#             cart_item['cart_key'] = cart_key
#             cart_item['product'] = products_map.get(item['product_id'])
#
#             # Skip if product no longer exists
#             if not cart_item['product']:
#                 continue
#
#             cart_item['price'] = Decimal(item['price'])
#             cart_item['base_price'] = Decimal(item.get('base_price', item['price']))
#             cart_item['total_price'] = cart_item['price'] * cart_item['quantity']
#
#             yield cart_item
#
#     def __len__(self):
#         """
#         Count total quantities.
#         """
#         return sum(item['quantity'] for item in self.cart.values())
#
#     def get_total_price(self):
#         """
#         Total price of cart.
#         """
#         return sum(
#             (Decimal(item['price']) * item['quantity'] for item in self.cart.values()),
#             Decimal('0.00')
#         )
#
#     def clear(self):
#         """
#         Clear cart.
#         """
#         if settings.CART_SESSION_ID in self.session:
#             del self.session[settings.CART_SESSION_ID]
#             self.save()