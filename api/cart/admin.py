from django.contrib import admin

from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email')
    ordering = ('-updated_at',)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cart',
        'product_variant',
        'quantity',
        'updated_at',
    )
    search_fields = (
        'product_variant__sku',
        'product_variant__name',
        'cart__user__username',
    )
    list_filter = ('cart',)
