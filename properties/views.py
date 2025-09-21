from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.conf import settings

from .models import Property
from .forms import ContactForm


def home(request):
    return render(request, "properties/home.html")


def properties(request):
    # Base query: only available properties, newest first
    properties = Property.objects.filter(is_available=True).order_by("-date_listed")

    # Filtering
    property_type = request.GET.get("property_type")
    listing_type = request.GET.get("listing_type")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    bedrooms = request.GET.get("bedrooms")
    bathrooms = request.GET.get("bathrooms")
    location = request.GET.get("location")

    if property_type:
        properties = properties.filter(property_type=property_type)
    if listing_type:
        properties = properties.filter(listing_type=listing_type)
    if min_price:
        properties = properties.filter(price__gte=min_price)
    if max_price:
        properties = properties.filter(price__lte=max_price)
    if bedrooms:
        properties = properties.filter(bedrooms=bedrooms)
    if location:
        properties = properties.filter(location=location)

    context = {
        "properties": properties,
        "property_types": Property.PROPERTY_TYPES,
        "listing_types": Property.LISTING_TYPES,
    }

    return render(request, "properties/properties.html", context)


def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    return render(request, "properties/property_detail.html", {"property": property})


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            # The email sending logic
            email_message = EmailMessage(
                subject=f"Contact Form Submission from {name}",
                body=message,
                from_email=settings.EMAIL_HOST_USER,
                to=[settings.CONTACT_EMAIL],
                reply_to=[email],
            )

            try:
                email_message.send()
            except Exception as e:
                return HttpResponse(f"Failed to send email: {e}")

            return redirect("properties:home")
    else:
        form = ContactForm()

    return render(request, "properties/contact.html", {"form": form})
