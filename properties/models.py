from django.db import models
from django.utils.text import slugify
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
    slug = models.SlugField(max_length=250, unique=True, blank=True)
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

    class Meta:
        verbose_name_plural = "Properties"
        ordering = [-date_listed]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

        if self.image:
            try:
                img = Image.open(self.image.path)
                if img.height > 600 or img.width > 800:
                    img.thumbnail((800, 600), Image.Resampling.LANCZOS)
                    img.save(self.image.path, optimize=True, quality=85)
            except Exception:
                pass  # Ignore errors, just save without resizing


# Multiple image gallery model
class PropertyImage(models.Model):
    property_obj = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="properties/")
    order = models.PositiveIntegerField(default=0)
    is_primary = models.BooleanField(default=False)

    class Meta:
        ordering = ["order"]


class Inquiry(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("in_progress", "In Progress"),
        ("closed", "Closed"),
    ]
    property_obj = models.ForeignKey(
        "Property",
        on_delete=models.CASCADE,
        related_name="inquiries",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        if self.property_obj:
            return f"Inquiry for {self.property_obj.title} by {self.name}"
        return f"General inquiry by {self.name}"
