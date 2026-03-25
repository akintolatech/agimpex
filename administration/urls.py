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
    # path('active_users/', views.active_users, name='active_users'),
    # path('dormant_users/', views.dormant_users, name='dormant_users'),

    # Category
    path('category_list/', views.category_list, name='category_list'),
    path('create_category/', views.create_category, name='create_category'),
    path('edit_category/<int:category_id>', views.edit_category, name='edit_category'),
    path('delete_category/<int:category_id>', views.delete_category, name='delete_category'),
]