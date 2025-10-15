from django.urls import path

from . import views


app_name = "properties"
urlpatterns = [
    path("", views.home, name="home"),
    path("properties/", views.properties, name="properties"),
    path("properties/<int:pk>/", views.property_detail, name="property_detail"),
    path("contact/", views.contact, name="contact"),  # General contact
    path("contact/<int:property_id>/", views.contact, name="contact"),  # Property inquiry
]
