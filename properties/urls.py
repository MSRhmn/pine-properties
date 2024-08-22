from django.urls import path

from . import views


app_name = "properties"
urlpatterns = [
    path("", views.home, name="home"),
    path("properties/", views.properties, name="properties"),
    path("contact/", views.contact, name="contact"),
]
