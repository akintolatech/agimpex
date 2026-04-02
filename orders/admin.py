from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Order, OrderItem



from django.contrib import admin
from .models import Order, OrderItem, OrderItemPropertyValue


class OrderItemPropertyValueInline(admin.TabularInline):
    model = OrderItemPropertyValue
    extra = 0
    readonly_fields = ('product_property', 'property_value', 'price_adjustment')
    can_delete = False


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'price', 'quantity')
    can_delete = False
    show_change_link = True


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'paid', 'created']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'price', 'quantity']
    inlines = [OrderItemPropertyValueInline]


@admin.register(OrderItemPropertyValue)
class OrderItemPropertyValueAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_item', 'product_property', 'property_value', 'price_adjustment']

# class OrderItemInline(admin.TabularInline):
#     model = OrderItem
#     raw_id_fields = ['product']
#
#
# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = [
#         'id',
#         'first_name',
#         'last_name',
#         'email',
#         'address',
#         'postal_code',
#         'city',
#         'paid',
#         'created',
#         'updated',
#     ]
#     list_filter = ['paid', 'created', 'updated']
#     inlines = [OrderItemInline]




