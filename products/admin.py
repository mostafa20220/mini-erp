from django.contrib import admin
from products.models import Product, StockChangeLog

class StockChangeLogInline(admin.TabularInline):
    model = StockChangeLog
    extra = 0
    can_delete = False
    readonly_fields = [
        'created_at', 'customer',
        'previous_qty', 'new_qty', 'change_reason'
    ]
    fields = [
        'created_at', 'customer',
        'previous_qty', 'new_qty', 'change_reason'
    ]

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku', 'name', 'category', 'cost_price', 'selling_price',
        'stock_qty', 'created_at'
    )
    list_filter = ('category', 'created_at', 'modified_at')
    search_fields = ('sku', 'name', 'category')
    readonly_fields = ('id', 'created_at', 'modified_at')
    ordering = ('-id',)

    fieldsets = (
        ('Product Information', {
            'fields': ('sku', 'name', 'category')
        }),
        ('Pricing', {
            'fields': ('cost_price', 'selling_price')
        }),
        ('Inventory', {
            'fields': ('stock_qty',)
        }),
        ('Metadata', {
            'fields': ( 'created_at', 'modified_at', 'created_by', 'modified_by'),
            'classes': ('collapse',)
        }),
    )

    inlines = [StockChangeLogInline]


@admin.register(StockChangeLog)
class StockChangeLogAdmin(admin.ModelAdmin):
    list_display = (
        'product', 'created_at', 'customer',
        'previous_qty', 'new_qty', 'change_reason'
    )
    list_filter = ('created_at', 'change_reason')
    search_fields = ('product__sku', 'product__name', 'customer__email', )
    readonly_fields = [
        'product', 'created_at', 'customer',
        'previous_qty', 'new_qty', 'change_reason'
    ]
    ordering = ('-created_at',)

    fieldsets = (
        ('Stock Change Information', {
            'fields': ('product', 'created_at', 'change_reason')
        }),
        ('Quantity Details', {
            'fields': ('previous_qty', 'new_qty')
        }),
        ('Related Users', {
            'fields': ('customer', )
        }),
    )


    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False



