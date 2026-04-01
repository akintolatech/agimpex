from django.db.models import Q
from django.shortcuts import render
from django.utils import translation
from shop.models import Product


# Create your views here.
def index(request):
    context = {
        "message": "Dreams Transcend various Lifetimes"
    }
    return render(request, 'website/index.html', context)


def about(request):
    return render(request, 'website/about.html')

def contact(request):
    return render(request, 'website/contact.html')

def services(request):
    return render(request, 'website/services.html')

def discount(request):
    return render(request, 'website/discount.html')

def natural_stones(request):
    return render(request, 'website/natural_stones.html')

def construction_goods(request):
    return render(request, 'website/construction.html')

def search_products(request):
    query = request.GET.get('q', '')
    products = []

    if query:
        # List all language fields for name and description
        search_fields = [
            'name_en', 'description_en',
            'name_hy', 'description_hy',
            'name_ru', 'description_ru',
        ]

        # Build dynamic Q objects
        q_objects = Q()
        for field in search_fields:
            q_objects |= Q(**{f"{field}__icontains": query})

        products = Product.objects.filter(q_objects).distinct()

    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'website/search.html', context)
