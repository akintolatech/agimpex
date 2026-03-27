from django.urls import path
from . import views
app_name = "website"

urlpatterns = [
    path('', views.index, name="index"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('services/', views.services, name="services"),
    path('discount/', views.discount, name="discount")
]