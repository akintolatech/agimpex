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

    #Product
    path('product_list/', views.product_list, name='product_list'),
    path('create_product/', views.create_product, name='create_product'),
    path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),


    # Product Property
    path('product_property_list/', views.product_property_list, name='product_property_list'),
    path('create_product_property/', views.create_product_property, name='create_product_property'),
    # path('edit_product_property/<int:property_id>', views.edit_product_property, name='edit_product_property'),
    # path('delete_product_property/<int:unit_id>', views.delete_product_property, name='delete_product_property'),


    # Unit of Measure
    path('unit_of_measure_list/', views.unit_of_measurement_list, name='unit_of_measure_list'),
    path('create_unit_of_measure/', views.create_unit_of_measure, name='create_unit_of_measure'),
    path('edit_unit_of_measure/<int:unit_id>', views.edit_unit_of_measure, name='edit_unit_of_measure'),
    path('delete_unit_of_measure/<int:unit_id>', views.delete_unit_of_measure, name='delete_unit_of_measure'),


]