from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

app_name = "administration"

urlpatterns = [
    # Add patterns here
    path('', views.administration_dashboard, name='administration'),

    # Users
    # path('users/', views.users, name='users'),
    path('user_details/<int:user_id>/', views.user_details, name='user_details'),

    # Orders
    path('order/<str:deposit_id>/', views.order_action, name='order_action'),
    path('order_list/', views.order_list, name='order_list'),


    # Category
    path('category_list/', views.category_list, name='category_list'),
    path('create_category/', views.create_category, name='create_category'),
    path('edit_category/<int:category_id>', views.edit_category, name='edit_category'),
    path('delete_category/<int:category_id>', views.delete_category, name='delete_category'),

    # Unit of Measure
    path('unit_of_measure_list/', views.unit_of_measurement_list, name='unit_of_measure_list'),
    # path('create_category/', views.create_category, name='create_category'),
    # path('edit_category/<int:category_id>', views.edit_category, name='edit_category'),
    # path('delete_category/<int:category_id>', views.delete_category, name='delete_category'),
]