from django.db import models

from common.models import BaseModel

"""
SKU
 CharField (unique)
Name
 CharField
Category
 CharField
Cost Price
 Decimal
Selling Price Decimal
Stock Qty
 Integer
"""

class Product(BaseModel):
    sku = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_qty = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} ({self.sku}) [ID: {self.pk}]"


class StockChangeLog(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='stock_change_logs')
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='stock_change_logs')
    sales_user = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='sales_stock_change_logs', null=True, blank=True)
    previous_qty = models.IntegerField()
    new_qty = models.IntegerField()
    change_reason = models.CharField(max_length=255)

    def __str__(self):
        return f"Stock change for {self.product.sku} at {self.created_at}"