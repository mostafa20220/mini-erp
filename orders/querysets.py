from django.db import models
from django.db.models import Q, Sum


class OrderQuerySet(models.QuerySet):
    """Custom QuerySet for Order model with business logic filters."""

    def pending(self):
        """Return pending orders."""
        return self.filter(status='PENDING')

    def confirmed(self):
        """Return confirmed orders."""
        return self.filter(status='CONFIRMED')

    def cancelled(self):
        """Return cancelled orders."""
        return self.filter(status='CANCELLED')

    def by_customer(self, customer):
        """Filter orders by customer."""
        if customer:
            return self.filter(customer=customer)
        return self

    def by_status(self, status):
        """Filter orders by status."""
        if status:
            return self.filter(status=status)
        return self

    def by_date_range(self, start_date=None, end_date=None):
        """Filter orders by date range."""
        queryset = self
        if start_date:
            queryset = queryset.filter(order_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(order_date__lte=end_date)
        return queryset

    def with_total_summary(self):
        """Annotate queryset with total amount summary."""
        return self.aggregate(
            total_orders=models.Count('id'),
            total_amount=Sum('total_amount')
        )


class OrderManager(models.Manager):
    """Custom manager for Order model."""

    def get_queryset(self):
        """Override to use OrderQuerySet."""
        return OrderQuerySet(self.model, using=self._db)

    def pending(self):
        """Return pending orders."""
        return self.get_queryset().pending()

    def confirmed(self):
        """Return confirmed orders."""
        return self.get_queryset().confirmed()

    def cancelled(self):
        """Return cancelled orders."""
        return self.get_queryset().cancelled()

    def by_customer(self, customer):
        """Filter orders by customer."""
        return self.get_queryset().by_customer(customer)

    def by_status(self, status):
        """Filter orders by status."""
        return self.get_queryset().by_status(status)


class OrderItemQuerySet(models.QuerySet):
    """Custom QuerySet for OrderItem model."""

    def by_order(self, order):
        """Filter items by order."""
        return self.filter(order=order)

    def by_product(self, product):
        """Filter items by product."""
        return self.filter(product=product)


class OrderItemManager(models.Manager):
    """Custom manager for OrderItem model."""

    def get_queryset(self):
        """Override to use OrderItemQuerySet."""
        return OrderItemQuerySet(self.model, using=self._db)

    def by_order(self, order):
        """Filter items by order."""
        return self.get_queryset().by_order(order)

    def by_product(self, product):
        """Filter items by product."""
        return self.get_queryset().by_product(product)

