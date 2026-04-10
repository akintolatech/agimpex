from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils import translation
from shop.models import Product
from django.shortcuts import render
from django.core.mail import EmailMessage
from django.conf import settings
from .forms import ContactForm
from django.contrib import messages

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



def send_message(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                name = form.cleaned_data['name']
                email = form.cleaned_data['email']
                subject = form.cleaned_data['subject']
                message = form.cleaned_data['message']
                uploaded_file = form.cleaned_data.get('file')

                full_message = f"""
                Name: {name}
                Email: {email}

                Message:
                {message}
                """

                mail = EmailMessage(
                    subject=subject,
                    body=full_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=['akintolatechnologies@gmail.com'],
                )

                if uploaded_file:
                    mail.attach(
                        uploaded_file.name,
                        uploaded_file.read(),
                        uploaded_file.content_type
                    )

                mail.send()

                messages.success(request, "Message sent successfully.")
                return redirect('website:index')

            except Exception as e:
                # Email sending or unexpected error
                messages.error(request, f"Error sending message: {str(e)}")
                return redirect('website:index')

        else:
            # Form validation errors
            errors = " ".join(
                [f"{field}: {','.join(err_list)}" for field, err_list in form.errors.items()]
            )
            messages.error(request, f"Form error: {errors}")
            return redirect('website:index')

    # If not POST
    messages.error(request, "Invalid request.")
    return redirect('website:index')