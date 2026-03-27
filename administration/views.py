from django.contrib.admin.views.decorators import staff_member_required
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

from administration.forms import EditCategoryForm, CreateCategoryForm, OrderApprovalForm
from orders.models import OrderItem
from shop.models import Category, UnitOfMeasure


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
            return redirect("administration:category_list") # Fixed typo here
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


#Unit of Measurement
@staff_member_required
def unit_of_measurement_list(request):

    context = {
        "unit_of_measurement": UnitOfMeasure.objects.all(),
    }

    return render(request, "administration/unitofmeasure/unitofmeasure_list.html", context)

#
# @staff_member_required
# def create_category(request):
#     if request.method == "POST":
#         form = CreateCategoryForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect("administration:category_list")
#     else:
#         form = CreateCategoryForm()
#
#     return render(request, "administration/category/create_category.html", {"form": form})
#
#
# @staff_member_required
# def edit_category(request, category_id):
#     category = get_object_or_404(Category, pk=category_id)
#
#     if request.method == "POST":
#         form = EditCategoryForm(request.POST, request.FILES, instance=category)
#         if form.is_valid():
#             form.save()
#             return redirect("administration:category_list") # Fixed typo here
#     else:
#         form = EditCategoryForm(instance=category)
#
#     context = {
#         "form": form,
#         "category": category
#     }
#     return render(request, "administration/category/edit_category.html", context)
#
#
# @staff_member_required
# def delete_category(request, category_id):
#     category = get_object_or_404(Category, pk=category_id)
#
#     if request.method == "POST":
#         category.delete()
#
#     return redirect("administration:category_list")

























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
