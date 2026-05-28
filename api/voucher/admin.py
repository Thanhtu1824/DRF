from django.contrib import admin

from .models import Voucher


@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'code',
        'name',
        'discount_type',
        'discount_value',
        'status',
        'start_at',
        'end_at',
        'used_count',
    )
    search_fields = ('code', 'name')
    list_filter = ('status', 'discount_type')
    ordering = ('-created_at',)
