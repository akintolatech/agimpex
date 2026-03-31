from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
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
import json

from administration.forms import EditCategoryForm, CreateCategoryForm, OrderApprovalForm, CreateUnitOfMeasureForm, \
    EditUnitOfMeasureForm, CreateProductPropertyForm, ProductForm
from orders.models import OrderItem
from shop.models import Category, UnitOfMeasure, ProductProperty, ProductPropertyValue, Product


@staff_member_required
def administration_dashboard(request):
    today = date.today()
    last_30_days = [today - timedelta(days=i) for i in range(30)]  # Fetch data for last 7 days
    #
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


@login_required
@transaction.atomic
@staff_member_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save()

            # Get all property names submitted
            property_names = request.POST.getlist('property_name[]')

            # Loop through each property
            for i, prop_name in enumerate(property_names):
                prop_name = prop_name.strip()

                if not prop_name:
                    continue

                # Create ProductProperty
                product_property = ProductProperty.objects.create(
                    product=product,
                    name=prop_name
                )

                # Get values for this property
                value_names = request.POST.getlist(f'property_values_{i}[]')
                value_adjustments = request.POST.getlist(f'property_price_adjustment_{i}[]')

                for j, value_name in enumerate(value_names):
                    value_name = value_name.strip()

                    if not value_name:
                        continue

                    price_adjustment = 0.00
                    if j < len(value_adjustments):
                        try:
                            price_adjustment = float(value_adjustments[j]) if value_adjustments[j] else 0.00
                        except ValueError:
                            price_adjustment = 0.00

                    ProductPropertyValue.objects.create(
                        product_property=product_property,
                        value=value_name,
                        price_adjustment=price_adjustment
                    )

            messages.success(request, 'Product created successfully.')
            return redirect('administration:create_product')

        else:
            messages.error(request, 'Please fix the errors below.')

    else:
        form = ProductForm()

    return render(request, 'administration/product/create_product.html', {'form': form})


@login_required
@transaction.atomic
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            product = form.save()

            submitted_property_ids = []
            submitted_value_ids = []

            property_ids = request.POST.getlist('property_id[]')
            property_names = request.POST.getlist('property_name[]')

            for i, prop_name in enumerate(property_names):
                prop_name = prop_name.strip()
                if not prop_name:
                    continue

                prop_id = property_ids[i].strip() if i < len(property_ids) else ''

                # Update existing property or create new one
                if prop_id:
                    product_property = ProductProperty.objects.filter(
                        id=prop_id,
                        product=product
                    ).first()

                    if product_property:
                        product_property.name = prop_name
                        product_property.save()
                    else:
                        product_property = ProductProperty.objects.create(
                            product=product,
                            name=prop_name
                        )
                else:
                    product_property = ProductProperty.objects.create(
                        product=product,
                        name=prop_name
                    )

                submitted_property_ids.append(product_property.id)

                # Values for this property block
                value_ids = request.POST.getlist(f'property_value_id_{i}[]')
                value_names = request.POST.getlist(f'property_values_{i}[]')
                value_adjustments = request.POST.getlist(f'property_price_adjustment_{i}[]')

                current_property_value_ids = []

                for j, value_name in enumerate(value_names):
                    value_name = value_name.strip()
                    if not value_name:
                        continue

                    value_id = value_ids[j].strip() if j < len(value_ids) else ''

                    try:
                        price_adjustment = float(value_adjustments[j]) if j < len(value_adjustments) and value_adjustments[j] else 0.00
                    except ValueError:
                        price_adjustment = 0.00

                    # Update existing value or create new one
                    if value_id:
                        property_value = ProductPropertyValue.objects.filter(
                            id=value_id,
                            product_property=product_property
                        ).first()

                        if property_value:
                            property_value.value = value_name
                            property_value.price_adjustment = price_adjustment
                            property_value.save()
                        else:
                            property_value = ProductPropertyValue.objects.create(
                                product_property=product_property,
                                value=value_name,
                                price_adjustment=price_adjustment
                            )
                    else:
                        property_value = ProductPropertyValue.objects.create(
                            product_property=product_property,
                            value=value_name,
                            price_adjustment=price_adjustment
                        )

                    current_property_value_ids.append(property_value.id)
                    submitted_value_ids.append(property_value.id)

                # Delete removed values for this property only
                product_property.property_values.exclude(id__in=current_property_value_ids).delete()

            # Delete removed properties (and cascade delete their values)
            product.properties.exclude(id__in=submitted_property_ids).delete()

            messages.success(request, 'Product updated successfully.')
            # return redirect('administration:edit_product', product_id=product.id)
            return redirect('administration:product_list')
        else:
            messages.error(request, 'Please fix the errors below.')

    else:
        form = ProductForm(instance=product)

    properties = product.properties.prefetch_related('property_values').all()

    context = {
        'form': form,
        'product': product,
        'properties': properties,
    }

    return render(request, 'administration/product/edit_product.html', context)


@login_required
@transaction.atomic
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
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
