from django.db import models
from django.core.validators import MinValueValidator

from common.models import BaseModel
from orders.constants import (
    ORDER_STATUS_PENDING,
    ORDER_STATUS_CONFIRMED,
    ORDER_STATUS_CANCELLED,
    ORDER_STATUS_CHOICES
)
from orders.querysets import OrderManager, OrderItemManager


class Order(BaseModel):
    order_number = models.CharField(
        max_length=50,
        unique=True,
        editable=False,
    )
    customer = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        related_name='orders',
    )
    order_date = models.DateField(
        auto_now_add=True,
    )
    status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS_CHOICES,
        default=ORDER_STATUS_PENDING,
    )
    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
    )

    objects = OrderManager()

    class Meta:
        db_table = 'orders_order'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-id']
        indexes = [
            models.Index(fields=['order_number']),
            models.Index(fields=['customer']),
            models.Index(fields=['status']),
            models.Index(fields=['order_date']),
            models.Index(fields=['created_by']),
        ]

    def __str__(self):
        return f"Order {self.order_number} - {self.customer.get_full_name() } [{self.status}]"

    @property
    def is_pending(self):
        return self.status == ORDER_STATUS_PENDING

    @property
    def is_confirmed(self):
        return self.status == ORDER_STATUS_CONFIRMED

    @property
    def is_cancelled(self):
        return self.status == ORDER_STATUS_CANCELLED

    @property
    def can_be_confirmed(self):
        return self.status == ORDER_STATUS_PENDING

    @property
    def can_be_cancelled(self):
        return self.status in [ORDER_STATUS_PENDING, ORDER_STATUS_CONFIRMED]

    def calculate_total(self):
        total = sum(item.total_price for item in self.items.all())
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.SET_NULL,
        related_name='order_items',
        null=True,
        blank=True,
    )
    product_name = models.CharField(
        max_length=255,
    )
    product_sku = models.CharField(
        max_length=100,
    )
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
    )
    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    objects = OrderItemManager()

    class Meta:
        db_table = 'orders_order_item'
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
        ordering = ['id']
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['product']),
        ]

    def __str__(self):
        return f"{self.product_name} x {self.quantity} (Order: {self.order.order_number})"

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.price
        super().save(*args, **kwargs)
