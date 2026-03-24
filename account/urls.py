from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views


urlpatterns = [

    path('', auth_views.LoginView.as_view(), name='login'),
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('dashboard/', views.dashboard, name='dashboard'),

]