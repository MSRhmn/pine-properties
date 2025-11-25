from django.contrib import admin
from django.utils.html import mark_safe

from .models import Property, Inquiry, PropertyImage


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 3
    fields = ("image", "order", "is_primary")


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyImageInline]
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


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "phone",
        "property_link",
        "status",
        "submitted_at",
    )
    list_filter = ("status", "submitted_at")
    search_fields = ("name", "email", "phone", "message")
    readonly_fields = ("submitted_at", "property_link")
    ordering = ("-submitted_at",)

    fieldsets = (
        ("Contact Information", {"fields": ("name", "email", "phone")}),
        (
            "Inquiry Details",
            {"fields": ("property_obj", "property_link", "message", "status")},
        ),
        ("Metadata", {"fields": ("submitted_at",)}),
    )

    def property_link(self, obj):
        if obj.property_obj:
            return mark_safe(
                f"<a href='/admin/properties/property/{obj.property_obj.id}/change/'>"
                f"{obj.property_obj.title}</a>"
            )
        return "General Inquiry"

    property_link.short_description = "Related Property"
