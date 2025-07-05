from django.db import models
from PIL import Image


class Property(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to="properties/")

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
