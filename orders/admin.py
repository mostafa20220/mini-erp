from django.contrib import admin
from orders.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['total_price']
    fields = ['product', 'product_name', 'product_sku', 'quantity', 'price', 'total_price']



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number', 'customer', 'order_date',
        'total_amount', 'created_by', 'created_at'
    )
    list_filter = ('status', 'order_date', 'created_at')
    search_fields = ('order_number', 'customer__email', 'customer__first_name', 'customer__last_name')
    readonly_fields = ('id', 'order_number', 'order_date', 'created_at', 'modified_at', 'total_amount')
    ordering = ('-id',)

    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'customer', 'order_date', 'status')
        }),
        ('Financial', {
            'fields': ('total_amount',)
        }),
        ('Metadata', {
            'fields': ( 'created_at', 'modified_at', 'created_by', 'modified_by'),
            'classes': ('collapse',)
        }),
    )

    inlines = [OrderItemInline]



@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'order', 'product_name', 'product_sku', 'quantity',
        'price', 'total_price'
    )
    list_filter = ('order__status',)
    search_fields = ('product_name', 'product_sku', 'order__order_number')
    readonly_fields = ('total_price',)
    ordering = ('-id',)

    fieldsets = (
        ('Order Information', {
            'fields': ('order',)
        }),
        ('Product Information', {
            'fields': ('product', 'product_name', 'product_sku')
        }),
        ('Pricing', {
            'fields': ('quantity', 'price', 'total_price')
        }),
    )
