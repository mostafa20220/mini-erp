from django.db import models

from common.models import BaseModel
from products.constants import OUT_OF_STOCK, LOW_STOCK, IN_STOCK, LOW_STOCK_THRESHOLD
from products.querysets import ProductManager


class Product(BaseModel):
    sku = models.CharField(
        max_length=100,
        unique=True,
        help_text='Unique product identifier (uppercase alphanumeric, hyphens, underscores)'
    )
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_qty = models.PositiveIntegerField()
    image = models.ImageField(
        upload_to='products/images/',
        null=True,
        blank=True,
    )

    objects = ProductManager()

    class Meta:
        db_table = 'products_product'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-id']
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['category']),
            models.Index(fields=['stock_qty']),
        ]

    def __str__(self):
        return f"{self.name} ({self.sku}) [ID: {self.pk}]"

    @property
    def stock_status(self):
        if self.stock_qty == 0:
            return OUT_OF_STOCK
        if self.stock_qty <= LOW_STOCK_THRESHOLD:
            return LOW_STOCK
        return IN_STOCK

    @property
    def profit_margin(self):
        if self.cost_price > 0:
            return ((self.selling_price - self.cost_price) / self.cost_price) * 100
        return 0


class StockChangeLog(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name='stock_change_logs', null=True, blank=True)
    product_name = models.CharField(max_length=255)
    product_category = models.CharField(max_length=100)
    product_sku = models.CharField(max_length=100)

    customer = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='stock_change_logs',null=True, blank=True)

    previous_qty = models.PositiveIntegerField()
    new_qty = models.PositiveIntegerField()

    change_reason = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='created_stock_change_logs')

    class Meta:
        db_table = 'products_stock_change_log'
        verbose_name = 'Stock Change Log'
        verbose_name_plural = 'Stock Change Logs'
        ordering = ['-id']
        indexes = [
            models.Index(fields=['product', '-created_at']),
            models.Index(fields=['customer']),
            models.Index(fields=['created_by']),
        ]

    def __str__(self):
        return f"Stock change for {self.product_sku} at {self.created_at} by {self.created_by.get_full_name()} for reason: {self.change_reason}"

    @property
    def quantity_change(self):
        return self.new_qty - self.previous_qty
