import django_filters

from products.constants import IN_STOCK, LOW_STOCK, OUT_OF_STOCK, STOCK_STATUS_CHOICES
from products.models import Product, StockChangeLog


class ProductFilter(django_filters.FilterSet):

    category = django_filters.CharFilter(field_name='category', lookup_expr='iexact')
    stock_status = django_filters.ChoiceFilter(
        method='filter_stock_status',
        choices=STOCK_STATUS_CHOICES,
    )
    min_price = django_filters.NumberFilter(field_name='selling_price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='selling_price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['category', 'stock_status', 'min_price', 'max_price']


    def filter_stock_status(self, queryset, name, value):

        if value == IN_STOCK:
            return queryset.in_stock()
        elif value == LOW_STOCK:
            return queryset.low_stock()
        elif value == OUT_OF_STOCK:
            return queryset.out_of_stock()
        return queryset


class StockChangeLogFilter(django_filters.FilterSet):

    product_id = django_filters.NumberFilter(field_name='product')
    customer_id = django_filters.NumberFilter(field_name='customer')
    sales_user_id = django_filters.NumberFilter(field_name='sales_user')

    class Meta:
        model = StockChangeLog
        fields = ['product_id', 'customer_id', 'sales_user_id']

