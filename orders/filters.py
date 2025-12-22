"""
Django-filter FilterSets for Order module.
"""
import django_filters
from orders.models import Order, OrderItem
from orders.constants import ORDER_STATUS_CHOICES


class OrderFilter(django_filters.FilterSet):
    """Filter for Order model."""

    status = django_filters.ChoiceFilter(
        field_name='status',
        choices=ORDER_STATUS_CHOICES
    )
    customer_id = django_filters.NumberFilter(field_name='customer__id')
    order_date_from = django_filters.DateFilter(field_name='order_date', lookup_expr='gte')
    order_date_to = django_filters.DateFilter(field_name='order_date', lookup_expr='lte')
    min_amount = django_filters.NumberFilter(field_name='total_amount', lookup_expr='gte')
    max_amount = django_filters.NumberFilter(field_name='total_amount', lookup_expr='lte')

    class Meta:
        model = Order
        fields = ['status', 'customer_id', 'order_date_from', 'order_date_to', 'min_amount', 'max_amount']


class OrderItemFilter(django_filters.FilterSet):
    """Filter for OrderItem model."""

    order_id = django_filters.NumberFilter(field_name='order__id')
    product_id = django_filters.NumberFilter(field_name='product__id')

    class Meta:
        model = OrderItem
        fields = ['order_id', 'product_id']

