from decimal import Decimal

from django.conf import settings
from shop.models import Product


class Cart:
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            # Save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def __iter__(self):
        """
        Iterate over the items in the cart and fetch the products
        from the database. Skip products that no longer exist.
        """
        product_ids = self.cart.keys()

        # Get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            # Skip cart items whose product no longer exists
            if 'product' not in item:
                continue

            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all quantities in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price),
            }

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def save(self):
        """
        Mark the session as modified to make sure it gets saved.
        """
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        """
        Remove cart from session.
        """
        if settings.CART_SESSION_ID in self.session:
            del self.session[settings.CART_SESSION_ID]
            self.save()

    def get_total_price(self):
        """
        Return the total cost of existing products only.
        This avoids counting deleted products still stored in session.
        """
        total = Decimal('0')
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            item = self.cart.get(str(product.id))
            if item:
                total += Decimal(item['price']) * item['quantity']

        return total