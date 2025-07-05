from django.contrib import admin
from django.utils.html import mark_safe

from .models import Property


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ("title", "location", "price", "image_preview")
    search_fields = ("title", "location")
    list_filter = ("location", "price")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" style="max-height: 100px;" />'
            )
        return "(No image)"

    image_preview.short_description = "Image Preview"
