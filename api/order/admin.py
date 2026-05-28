from django.contrib import admin

from .models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'address',
        'status',
        'total_price',
        'final_price',
        'created_at',
    )
    search_fields = (
        'id',
        'user__username',
        'user__email',
    )
    list_filter = ('status',)
    ordering = ('-created_at',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'product',
        'variant',
        'quantity',
        'unit_price',
        'subtotal',
        'created_at',
    )
    search_fields = (
        'order__id',
        'product__name',
        'variant__sku',
    )
    list_filter = ('order',)
    ordering = ('-id',)
