from django.db import models

from api.brand.models import Brand
from api.category.models  import Category
from django.conf import settings


class Product (models.Model):
    STATUS_ACTIVE = "active"
    STATUS_INACTIVE = "inactive"
    STATUS_SOLD_OUT = "sold_out"

    STATUS_CHOICES = [
        (STATUS_ACTIVE, "Active"),
        (STATUS_INACTIVE, "Inactive"),
        (STATUS_SOLD_OUT, "Sold out"),
    ]
    name = models.CharField(max_length = 100)
    seller = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name="products",
)
    category = models.ForeignKey(Category,
        on_delete = models.CASCADE,
        related_name = "products",)
    brand = models.ForeignKey(Brand,
        on_delete = models.CASCADE,
        related_name = "products",)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    thumbnail_url = models.URLField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_ACTIVE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name