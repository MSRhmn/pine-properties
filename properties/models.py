from django.db import models
from PIL import Image


class Property(models.Model):
    PROPERTY_TYPES = [
        ("house", "House"),
        ("apartment", "Apartment"),
        ("condo", "Condominium"),
        ("townhouse", "Townhouse"),
        ("land", "Land"),
    ]

    LISTING_TYPES = [
        ("sale", "For Sale"),
        ("rent", "For Rent"),
    ]

    title = models.CharField(max_length=200)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPES)
    location = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.PositiveIntegerField(default=1)
    bathrooms = models.PositiveIntegerField(default=1)
    square_feet = models.PositiveIntegerField(null=True, blank=True)
    image = models.ImageField(upload_to="properties/")
    is_available = models.BooleanField(default=True)
    date_listed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            try:
                img = Image.open(self.image.path)
                if img.height > 600 or img.width > 800:
                    img.thumbnail((800, 600), Image.Resampling.LANCZOS)
                    img.save(self.image.path, optimize=True, quality=85)
            except Exception:
                pass  # Ignore errors, just save without resizing
