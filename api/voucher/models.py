from django.db import models


class Voucher(models.Model):
    TYPE_PERCENT = 'percent'
    TYPE_FIXED = 'fixed'

    TYPE_CHOICES = [
        (TYPE_PERCENT, 'Percent'),
        (TYPE_FIXED, 'Fixed'),
    ]

    STATUS_ACTIVE = 'active'
    STATUS_INACTIVE = 'inactive'
    STATUS_EXPIRED = 'expired'

    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_INACTIVE, 'Inactive'),
        (STATUS_EXPIRED, 'Expired'),
    ]

    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    discount_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default=TYPE_PERCENT,
    )
    discount_value = models.DecimalField(max_digits=12, decimal_places=2)
    min_order_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )
    max_discount_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
    )
    usage_limit = models.PositiveIntegerField(blank=True, null=True)
    used_count = models.PositiveIntegerField(default=0)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_ACTIVE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['status']),
            models.Index(fields=['start_at', 'end_at']),
        ]

    def __str__(self):
        return self.code
