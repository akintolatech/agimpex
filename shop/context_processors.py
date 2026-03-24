from .models import Category, Product

def product_list(request):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    return {
        'category': category,
        'categories': categories,
        'products': products,
    }