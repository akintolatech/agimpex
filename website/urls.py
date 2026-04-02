from django.urls import path
from . import views
app_name = "website"

urlpatterns = [
    path('', views.index, name="index"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('services/', views.services, name="services"),
    path('discount/', views.discount, name="discount"),
    path('search/', views.search_products, name='search'),
    path('natural_stones/', views.natural_stones, name='natural_stones'),
    path('construction_goods/', views.construction_goods, name='construction_goods'),

]