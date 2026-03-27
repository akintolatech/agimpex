from django.shortcuts import render

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
