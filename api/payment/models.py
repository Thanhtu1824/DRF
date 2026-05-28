from django.db import models

from api.order.models import Order


class Payment(models.Model):
    METHOD_COD = 'cod'
    METHOD_BANK_TRANSFER = 'bank_transfer'
    METHOD_MOMO = 'momo'
    METHOD_VNPAY = 'vnpay'

    METHOD_CHOICES = [
        (METHOD_COD, 'Cash on Delivery'),
        (METHOD_BANK_TRANSFER, 'Bank Transfer'),
        (METHOD_MOMO, 'MoMo'),
        (METHOD_VNPAY, 'VNPay'),
    ]

    STATUS_PENDING = 'pending'
    STATUS_PAID = 'paid'
    STATUS_FAILED = 'failed'
    STATUS_REFUNDED = 'refunded'
    STATUS_DELETED = 'deleted'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_PAID, 'Paid'),
        (STATUS_FAILED, 'Failed'),
        (STATUS_REFUNDED, 'Refunded'),
        (STATUS_DELETED, 'Deleted'),
    ]

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='payments',
    )
    payment_method = models.CharField(max_length=30, choices=METHOD_CHOICES)
    payment_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payments'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['payment_status']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f'Payment #{self.id} - Order #{self.order_id}'
