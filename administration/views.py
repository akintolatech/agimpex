from decimal import Decimal, InvalidOperation

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.urls import reverse
from django.contrib import messages
from account.models import Profile
from django.db.models.functions import TruncDate
from django.db.models import Count, Sum
from datetime import date, timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render
# from .forms import DepositApprovalForm, WithdrawApprovalForm, WhatsappScreenshotApprovalForm
# import json


from administration.forms import EditCategoryForm, CreateCategoryForm, OrderApprovalForm, CreateUnitOfMeasureForm, \
    EditUnitOfMeasureForm, CreateProductPropertyForm, ProductForm
from orders.models import OrderItem
from shop.models import Category, UnitOfMeasure, ProductProperty, Product, ProductPricing, ProductPropertyValue

@login_required(login_url='login')
# @user_passes_test(is_staff_user, login_url='login')
@staff_member_required
def administration_dashboard(request):
    today = date.today()
    last_30_days = [today - timedelta(days=i) for i in range(30)]  # Fetch data for last 7 days

    # # Fetching counts per day
    # deposits = (
    #     Deposit.objects.filter(created__gte=min(last_30_days))
    #     .annotate(day=TruncDate("created"))
    #     .values("day")
    #     .annotate(count=Count("id"))
    # )
    #
    # withdrawals = (
    #     Withdraw.objects.filter(created__gte=min(last_30_days))
    #     .annotate(day=TruncDate("created"))
    #     .values("day")
    #     .annotate(count=Count("id"))
    # )
    #
    # transfers = (
    #     Transfer.objects.filter(created__gte=min(last_30_days))
    #     .annotate(day=TruncDate("created"))
    #     .values("day")
    #     .annotate(count=Count("id"))
    # )

    # # Convert counts to dictionaries
    # deposit_counts = {entry["day"].strftime("%Y-%m-%d"): entry["count"] for entry in deposits}
    # withdrawal_counts = {entry["day"].strftime("%Y-%m-%d"): entry["count"] for entry in withdrawals}
    # transfer_counts = {entry["day"].strftime("%Y-%m-%d"): entry["count"] for entry in transfers}
    #
    # days = [day.strftime("%Y-%m-%d") for day in reversed(last_30_days)]
    # daily_deposits = [deposit_counts.get(day, 0) for day in days]
    # daily_withdrawals = [withdrawal_counts.get(day, 0) for day in days]
    # daily_transfers = [transfer_counts.get(day, 0) for day in days]
    #
    # # Compute total sums
    # total_deposit_amount = Deposit.objects.aggregate(total=Sum("amount"))["total"] or 0
    # total_withdraw_amount = Withdraw.objects.aggregate(total=Sum("amount"))["total"] or 0
    # total_transfer_amount = Transfer.objects.aggregate(total=Sum("amount"))["total"] or 0

    context = {
        # "total_deposits": Deposit.objects.count(),
        # "total_withdrawals": Withdraw.objects.count(),
        # "total_transfer": Transfer.objects.count(),
        # "total_deposit_amount": total_deposit_amount,  # Total sum of deposits
        # "total_withdraw_amount": total_withdraw_amount,  # Total sum of withdrawals
        # "total_transfer_amount": total_transfer_amount,  # Total sum of transfers
        # "days": json.dumps(days),
        # "daily_deposits": json.dumps(daily_deposits),
        # "daily_withdrawals": json.dumps(daily_withdrawals),
        # "daily_transfers": json.dumps(daily_transfers),
    }

    return render(request, "administration/administration_dashboard.html", context)


# Users
@staff_member_required
def user_details(request, user_id):
    user_account = get_object_or_404(Profile, id=user_id)

    context = {
        "user_account": user_account,
    }
    return render(request, "administration/users/user_details.html", context)

#Orders
@staff_member_required
def order_list(request):

    context = {
        "order_item": OrderItem.objects.all(),
    }

    return render(request, "administration/order/order_list.html", context)

@staff_member_required
def order_action(request, order_id):
    order_request = get_object_or_404(OrderItem, reference_code=order_id)

    if request.method == "POST":
        form = OrderApprovalForm(request.POST, instance=order_request)
        if form.is_valid():
            form.save()
            return redirect('administration:order_list')

    else:
        form = OrderApprovalForm(instance=order_request)

    context = {
        "form": form,
        "order_request": order_request
    }

    return render(request, "administration/order/approve_order.html", context)

# Category
@staff_member_required
def category_list(request):

    context = {
        "categories": Category.objects.all(),
    }

    return render(request, "administration/category/category_list.html", context)


@staff_member_required
def create_category(request):
    if request.method == "POST":
        form = CreateCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("administration:category_list")
    else:
        form = CreateCategoryForm()

    return render(request, "administration/category/create_category.html", {"form": form})


@staff_member_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)

    if request.method == "POST":
        form = EditCategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect("administration:category_list")
    else:
        form = EditCategoryForm(instance=category)

    context = {
        "form": form,
        "category": category
    }
    return render(request, "administration/category/edit_category.html", context)


@staff_member_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)

    if request.method == "POST":
        category.delete()

    return redirect("administration:category_list")



#Product
@staff_member_required
def product_list(request):

    context = {
        "products": Product.objects.all(),
    }

    return render(request, "administration/product/product_list.html", context)


@transaction.atomic
def save_or_rebuild_product_pricing_structure(request, product, rebuild=False):
    """
    Save or rebuild product properties, property values, and pricing rows.

    If rebuild=True:
        - delete old pricing rows
        - delete old properties (which cascades property values)
        - recreate from POST data
    """

    if rebuild:
        # Delete old pricing rows first (M2M links auto-clear)
        product.pricing_rows.all().delete()

        # Delete old properties (cascades ProductPropertyValue)
        product.properties.all().delete()

    property_names = [p.strip() for p in request.POST.getlist('property_names[]') if p.strip()]

    # If no properties submitted, leave product as simple/base-price product
    if not property_names:
        return

    # Create properties in exact order
    property_objects = []
    for prop_name in property_names:
        prop = ProductProperty.objects.create(product=product, name=prop_name)
        property_objects.append(prop)

    row_prices = request.POST.getlist('row_price[]')
    row_count = len(row_prices)

    # Cache values per property to avoid duplicate ProductPropertyValue creation
    # key = (property_id, value_lower)
    value_cache = {}

    for row_index in range(row_count):
        selected_values = []

        # For each property column, get the row's value
        for col_index, prop_obj in enumerate(property_objects):
            column_values = request.POST.getlist(f'row_val_{col_index}[]')

            if row_index >= len(column_values):
                continue

            raw_value = column_values[row_index].strip()
            if not raw_value:
                continue

            cache_key = (prop_obj.id, raw_value.lower())

            if cache_key in value_cache:
                value_obj = value_cache[cache_key]
            else:
                value_obj, _ = ProductPropertyValue.objects.get_or_create(
                    product_property=prop_obj,
                    value=raw_value
                )
                value_cache[cache_key] = value_obj

            selected_values.append(value_obj)

        # Price for this row
        raw_price = row_prices[row_index].strip() if row_index < len(row_prices) else ''
        if not raw_price:
            continue

        try:
            final_price = Decimal(raw_price)
        except (InvalidOperation, TypeError):
            continue

        pricing = ProductPricing.objects.create(
            product=product,
            price=final_price
        )

        if selected_values:
            pricing.property_values.set(selected_values)



@transaction.atomic
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                product = form.save()
                save_or_rebuild_product_pricing_structure(request, product, rebuild=False)
                messages.success(request, f'{product.name} created successfully.')
                return redirect('administration:product_list')
            else:
                messages.error(request, 'Please fix the form errors.')
        except Exception as e:
            messages.error(request, f'Error creating product: {str(e)}')
    else:
        form = ProductForm()

    context = {
        'form': form,
        'existing_pricing_data': None,
    }
    return render(request, 'administration/product/create_product.html', context)
# def create_product(request):
#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES)
#
#         try:
#             if form.is_valid():
#                 product = form.save()
#
#                 # Save dynamic properties + pricing
#                 save_or_rebuild_product_pricing_structure(request, product, rebuild=False)
#
#                 messages.success(request, f'{ product.name }Product created successfully.')
#                 return redirect('administration:product_list')
#             else:
#                 messages.error(request, 'Please fix the form errors.')
#
#         except Exception as e:
#             messages.error(request, f'Error creating product: {str(e)}')
#     else:
#         form = ProductForm()
#
#     context = {
#         'form': form,
#     }
#
#     return render(request, 'administration/product/create_product.html', context)


@transaction.atomic
@transaction.atomic
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        try:
            if form.is_valid():
                product = form.save()
                save_or_rebuild_product_pricing_structure(request, product, rebuild=True)
                messages.success(request, f'{product.name} updated successfully.')
                return redirect('administration:product_list')
            else:
                messages.error(request, 'Please fix the form errors.')
        except Exception as e:
            messages.error(request, f'Error updating product: {str(e)}')
    else:
        form = ProductForm(instance=product)

    # Build existing data for JS
    properties = list(product.properties.all().order_by('id'))
    existing_pricing_data = {
        'properties': [
            {'en': p.name, 'hy': p.name_hy, 'ru': p.name_ru} for p in properties
        ],
        'rows': []
    }

    for pricing in product.pricing_rows.prefetch_related('property_values', 'property_values__product_property'):
        row_map = {pv.product_property_id: pv.value for pv in pricing.property_values.all()}
        ordered_values = [row_map.get(p.id, '') for p in properties]
        existing_pricing_data['rows'].append({
            'values': ordered_values,
            'price': str(pricing.price)
        })

    context = {
        'form': form,
        'product': product,
        'existing_pricing_data': existing_pricing_data,
    }
    return render(request, 'administration/product/edit_product.html', context)


# def edit_product(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#
#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES, instance=product)
#
#         try:
#             if form.is_valid():
#                 product = form.save()
#
#                 # Rebuild pricing structure from submitted form
#                 save_or_rebuild_product_pricing_structure(request, product, rebuild=True)
#
#                 messages.success(request, f'{product.name} updated successfully.')
#                 return redirect('administration:product_list')
#             else:
#                 messages.error(request, 'Please fix the form errors.')
#
#         except Exception as e:
#             messages.error(request, f'Error updating product: {str(e)}')
#     else:
#         form = ProductForm(instance=product)
#
#     # Build existing data for edit template JS
#     properties = list(product.properties.all().order_by('id'))
#
#     existing_pricing_data = {
#         'properties': [prop.name for prop in properties],
#         'rows': []
#     }
#
#     pricing_rows = product.pricing_rows.prefetch_related(
#         'property_values',
#         'property_values__product_property'
#     ).all()
#
#     for pricing in pricing_rows:
#         row_map = {}
#
#         for pv in pricing.property_values.all():
#             row_map[pv.product_property_id] = pv.value
#
#         ordered_values = []
#         for prop in properties:
#             ordered_values.append(row_map.get(prop.id, ''))
#
#         existing_pricing_data['rows'].append({
#             'values': ordered_values,
#             'price': str(pricing.price)
#         })
#
#     context = {
#         'product': product,
#         'form': form,
#         'existing_pricing_data': existing_pricing_data,
#     }
#
#     return render(request, 'administration/product/edit_product.html', context)
#
#
@login_required
@transaction.atomic
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product.delete()
        messages.success(request, f'{product.name} deleted successfully.')
        return redirect('administration:product_list')

    return redirect('administration:product_list')


#Product Property
@staff_member_required
def product_property_list(request):

    context = {
        "product_property": ProductProperty.objects.all(),
    }

    return render(request, "administration/product/productproperty_list.html", context)


@staff_member_required
def create_product_property(request):
    if request.method == "POST":
        form = CreateProductPropertyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("administration:product_property_list")
    else:
        form = CreateProductPropertyForm()

    return render(request, "administration/product/create_productproperty.html", {"form": form})


# @staff_member_required
# def edit_unit_of_measure(request, unit_id):
#     unit_of_measure = get_object_or_404(UnitOfMeasure, pk=unit_id)
#
#     if request.method == "POST":
#         form = EditUnitOfMeasureForm(request.POST, instance=unit_of_measure)
#         if form.is_valid():
#             form.save()
#             return redirect("administration:unit_of_measure_list")
#     else:
#         form = EditUnitOfMeasureForm(instance=unit_of_measure)
#
#     context = {
#         "form": form,
#         "unit_of_measure": unit_of_measure
#     }
#     return render(request, "administration/unitofmeasure/edit_unitofmeasure.html",context)
#
#
# @staff_member_required
# def delete_unit_of_measure(request, unit_id):
#     unit_of_measure = get_object_or_404(UnitOfMeasure, pk=unit_id)
#
#     if request.method == "POST":
#         unit_of_measure.delete()
#
#     return redirect("administration:unit_of_measure_list")
#



#Unit of Measurement
@staff_member_required
def unit_of_measurement_list(request):

    context = {
        "unit_of_measurement": UnitOfMeasure.objects.all(),
    }

    return render(request, "administration/unitofmeasure/unitofmeasure_list.html", context)


@staff_member_required
def create_unit_of_measure(request):
    if request.method == "POST":
        form = CreateUnitOfMeasureForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("administration:unit_of_measure_list")
    else:
        form = CreateUnitOfMeasureForm()

    return render(request, "administration/unitofmeasure/create_unitofmeasure.html", {"form": form})


@staff_member_required
def edit_unit_of_measure(request, unit_id):
    unit_of_measure = get_object_or_404(UnitOfMeasure, pk=unit_id)

    if request.method == "POST":
        form = EditUnitOfMeasureForm(request.POST, instance=unit_of_measure)
        if form.is_valid():
            form.save()
            return redirect("administration:unit_of_measure_list")
    else:
        form = EditUnitOfMeasureForm(instance=unit_of_measure)

    context = {
        "form": form,
        "unit_of_measure": unit_of_measure
    }
    return render(request, "administration/unitofmeasure/edit_unitofmeasure.html",context)


@staff_member_required
def delete_unit_of_measure(request, unit_id):
    unit_of_measure = get_object_or_404(UnitOfMeasure, pk=unit_id)

    if request.method == "POST":
        unit_of_measure.delete()

    return redirect("administration:unit_of_measure_list")


























# def active_users(request):
#
#     active_users_list = Profile.objects.filter(account_status=Profile.AccountStatus.ACTIVE)
#
#     context = {
#         "active_users_list": active_users_list,
#     }
#     return render(request, "administration/users/active_users.html", context)



# def users(request):
#
#
#     context = {
#         "total_users": Profile.objects.count(),
#         "profiles": Profile.objects.all(),
#         "total_active_users": Profile.objects.filter(account_status=Profile.AccountStatus.ACTIVE).count(),
#         "total_dormant_users": Profile.objects.filter(account_status=Profile.AccountStatus.DORMANT).count(),
#         "active_users": active_users,
#         "dormant_users": dormant_users,
#     }
#     return render(request, "administration/users/admin_users.html", context)
#
#

# @staff_member_required
# def dormant_users(request):
#
#     dormant_users_list = Profile.objects.filter(account_status=Profile.AccountStatus.DORMANT)
#
#     context = {
#         "dormant_users_list": dormant_users_list,
#     }
#     return render(request, "administration/users/dormant_users.html", context)
