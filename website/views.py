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

def gallery(request):
    return render(request, 'website/gallery.html')

def discount(request):
    return render(request, 'website/discount.html')
