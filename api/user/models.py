from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_ADMIN = 'admin'
    ROLE_STAFF = 'staff'
    ROLE_SELLER = 'seller'
    ROLE_CUSTOMER = 'customer'

    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_STAFF, 'Staff'),
        (ROLE_SELLER, 'Seller'),
        (ROLE_CUSTOMER, 'Customer'),
    ]

    BACK_OFFICE_ROLES = [
        ROLE_ADMIN,
        ROLE_STAFF,
    ]

    SALES_ROLES = [
        ROLE_ADMIN,
        ROLE_STAFF,
        ROLE_SELLER,
    ]

    STATUS_ACTIVE = 'active'
    STATUS_INACTIVE = 'inactive'

    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_INACTIVE, 'Inactive'),
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

    def is_admin_role(self):
        return self.role == self.ROLE_ADMIN

    def is_staff_role(self):
        return self.role == self.ROLE_STAFF

    def is_seller_role(self):
        return self.role == self.ROLE_SELLER

    def is_customer_role(self):
        return self.role == self.ROLE_CUSTOMER

    def can_access_back_office(self):
        return self.role in self.BACK_OFFICE_ROLES

    def can_manage_sales_catalog(self):
        return self.role in self.SALES_ROLES

    def _sync_auth_flags(self):
        self.is_superuser = self.is_admin_role()
        self.is_staff = self.can_access_back_office()
        self.is_active = self.status == self.STATUS_ACTIVE

    def save(self, *args, **kwargs):
        self._sync_auth_flags()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class UserAddress(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='addresses',
    )
    recipient_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address_line = models.CharField(max_length=255)
    ward = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    province = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_default', '-updated_at']
        indexes = [models.Index(fields=['user', 'is_default'])]

    def __str__(self):
        return f'{self.recipient_name} - {self.province}'
