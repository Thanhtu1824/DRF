from django.contrib.auth.models import AbstractUser
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
    
# -------------------------------------------------

class User(AbstractUser):
    ROLE_ADMIN = "admin"
    ROLE_SELLER = "seller"
    ROLE_CUSTOMER = "customer"

    ROLE_CHOICES = [
        (ROLE_ADMIN, "Admin"),
        (ROLE_SELLER, "Seller"),
        (ROLE_CUSTOMER, "Customer"),
    ]

    STATUS_ACTIVE = "active"
    STATUS_BLOCKED = "blocked"

    STATUS_CHOICES = [
        (STATUS_ACTIVE, "Active"),
        (STATUS_BLOCKED, "Blocked"),
    ]

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_CUSTOMER,
    )
    avatar = models.URLField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_ACTIVE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.username