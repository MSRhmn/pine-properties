from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.conf import settings

from .models import Property
from .forms import ContactForm


def home(request):
    return render(request, "properties/home.html")


def properties(request):
    properties = Property.objects.all()
    return render(request, "properties/properties.html", {"properties": properties})


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
