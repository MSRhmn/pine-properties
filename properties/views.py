from django.shortcuts import render, redirect
from django.core.mail import send_mail

from .models import Property
from .forms import ContactForm


def home(request):
    return render(request, "properties/home.html")


def properties(request):
    properties = Property.objects.all()
    return render(request, "properties/properties.html", {"properties": properties})


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            # The email sending logic
            send_mail(
                f"Contact Form Submission from {name}",
                message,
                email,
                ["privateworkprovider@gmail.com"],
            )
            return redirect("properties:home")
    else:
        form = ContactForm()

    return render(request, "properties/contact.html", {"form": form})
