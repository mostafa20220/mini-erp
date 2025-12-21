from django.contrib import admin

from products.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name', 'category', 'cost_price', 'selling_price', 'stock_qty')
    search_fields = ('sku', 'name', 'category')
    list_filter = ('category',)
    ordering = ('sku',)
    readonly_fields = ('id',)


