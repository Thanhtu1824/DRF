from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'payment_method',
        'payment_status',
        'amount',
        'paid_at',
        'created_at',
        'is_fund_in',
        'fund_in_at',
        'fund_in_by',
    )
    search_fields = ('order__id',)
    list_filter = ('payment_method', 'payment_status', 'is_fund_in')
    ordering = ('-created_at', '-fund_in_at')
