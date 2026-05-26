
from django.db import models

# Create your models here.

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
