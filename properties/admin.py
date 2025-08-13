from django.contrib import admin
from django.utils.html import mark_safe

from .models import Property


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "location",
        "price",
        "image_preview",
        "property_type",
        "listing_type",
        "is_available",
    )
    search_fields = ("title", "location")
    list_filter = ("property_type", "listing_type", "is_available")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" style="max-height: 100px;" />'
            )
        return "(No image)"

    image_preview.short_description = "Image Preview"
