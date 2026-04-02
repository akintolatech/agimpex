from decimal import Decimal
from django.db import models
from shop.models import Product


class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)

    paid = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum((item.get_cost() for item in self.items.all()), Decimal('0.00'))


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        related_name='order_items',
        on_delete=models.PROTECT
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)  # final unit price
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return f'OrderItem #{self.id} - {self.product.name}'

    def get_cost(self):
        return self.price * self.quantity


class OrderItemPropertyValue(models.Model):
    order_item = models.ForeignKey(
        OrderItem,
        related_name='selected_properties',
        on_delete=models.CASCADE
    )
    product_property = models.CharField(max_length=100)
    property_value = models.CharField(max_length=100)
    price_adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = 'Order Item Property Value'
        verbose_name_plural = 'Order Item Property Values'

    def __str__(self):
        return f"{self.product_property}: {self.property_value}"






# import uuid
#
# from django.db import models
#
#
# class Order(models.Model):
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     email = models.EmailField()
#     address = models.CharField(max_length=250)
#     postal_code = models.CharField(max_length=20)
#     city = models.CharField(max_length=100)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#     paid = models.BooleanField(default=False)
#
#     class Meta:
#         ordering = ['-created']
#         indexes = [
#             models.Index(fields=['-created']),
#         ]
#
#     def __str__(self):
#         return f'Order {self.id}'
#
#     def get_total_cost(self):
#         return sum(item.get_cost() for item in self.items.all())
#
#
# class OrderItem(models.Model):
#     order = models.ForeignKey(
#         Order,
#         related_name='items',
#         on_delete=models.CASCADE
#     )
#     product = models.ForeignKey(
#         'shop.Product',
#         related_name='order_items',
#         on_delete=models.CASCADE
#     )
#     price = models.DecimalField(
#         max_digits=10,
#         decimal_places=2
#     )
#     quantity = models.PositiveIntegerField(default=1)
#
#     reference_code = models.CharField(max_length=12, unique=True, blank=True)
#
#     def __str__(self):
#         return str(self.id)
#
#     def get_cost(self):
#         return self.price * self.quantity
#
#     def save(self, *args, **kwargs):
#         from account.models import Profile  # Import inside to prevent circular imports
#
#         if not self.reference_code:
#             self.reference_code = str(uuid.uuid4())[:12]  # Generate unique 12-character code
#
#         super().save(*args, **kwargs)