from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.conf import settings

from .models import Property, Inquiry
from .forms import ContactForm


def home(request):
    featured_properties = Property.objects.filter(is_available=True).order_by(
        "-date_listed"
    )[:3]
    return render(
        request, "properties/home.html", {"featured_properties": featured_properties}
    )


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
    if bathrooms:
        properties = properties.filter(bathrooms=bathrooms)
    if location:
        properties = properties.filter(location=location)

    # Pagination
    paginator = Paginator(properties, 6)  # Show 6 properties per page
    page_number = request.GET.get("page")
    properties_page = paginator.get_page(page_number)

    context = {
        "properties": properties_page,
        "property_types": Property.PROPERTY_TYPES,
        "listing_types": Property.LISTING_TYPES,
        "paginator": paginator,
    }

    return render(request, "properties/properties.html", context)


def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    return render(request, "properties/property_detail.html", {"property": property})


def contact(request, property_id=None):
    """Handles both general contact and property-specific inquiries."""
    related_property = None

    if property_id:
        related_property = get_object_or_404(Property, id=property_id)

    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            # Save inquiry in database
            inquiry = Inquiry.objects.create(
                property_obj=related_property,
                name=form.cleaned_data["name"],
                email=form.cleaned_data["email"],
                phone=form.cleaned_data.get("phone", ""),
                message=form.cleaned_data["message"],
            )

            # Send email notification
            subject = (
                f"Inquiry for {related_property.title}"
                if related_property
                else "General contact"
            )
            email_body = (
                f"Name: {inquiry.name}\n"
                f"Email: {inquiry.email}\n"
                f"Phone: {inquiry.phone}\n\n"
                f"Message:\n{inquiry.message}"
            )

            if related_property:
                email_body = f"Property: {related_property.title}\n\n{email_body}"

            # The email sending logic
            email_message = EmailMessage(
                subject=subject,
                body=email_body,
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
