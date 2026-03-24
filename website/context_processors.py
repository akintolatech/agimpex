# website/context_processors.py
from .models import WebDetails, LandingContent


def web_details(request):
    # Fetch the first WebDetails object
    details = WebDetails.objects.first()
    landing = LandingContent.objects.all()
    return {
        'business': details,
        'landing': landing
    }