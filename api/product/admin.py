from django.contrib import admin

from .models import Product, ProductVariant


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'created_at')
    search_fields = ('name',)


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'product',
        'name',
        'sku',
        'price',
        'stock',
        'updated_at',
    )
    search_fields = ('name', 'sku', 'product__name')
    list_filter = ('product',)
