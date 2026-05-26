
from django.db import models

# Create your models here.

class Brand(models.Model):
    name = models.CharField(max_length=100)
    logo_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# -------------------------------------------------

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey("self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
