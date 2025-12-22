from django.db import models
from django.db.models import Sum
from orders.constants import ORDER_STATUS_PENDING, ORDER_STATUS_CONFIRMED, ORDER_STATUS_CANCELLED


class OrderQuerySet(models.QuerySet):

    def pending(self):
        return self.filter(status=ORDER_STATUS_PENDING)

    def confirmed(self):
        return self.filter(status=ORDER_STATUS_CONFIRMED)

    def cancelled(self):
        return self.filter(status=ORDER_STATUS_CANCELLED)

    def by_customer(self, customer):
        if customer:
            return self.filter(customer=customer)
        return self

    def by_status(self, status):
        if status:
            return self.filter(status=status)
        return self

    def by_date_range(self, start_date=None, end_date=None):
        queryset = self
        if start_date:
            queryset = queryset.filter(order_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(order_date__lte=end_date)
        return queryset

    def with_total_summary(self):
        return self.aggregate(
            total_orders=models.Count('id'),
            total_amount=Sum('total_amount')
        )


class OrderManager(models.Manager):

    def get_queryset(self):
        return OrderQuerySet(self.model, using=self._db)

    def pending(self):
        return self.get_queryset().pending()

    def confirmed(self):
        return self.get_queryset().confirmed()

    def cancelled(self):
        return self.get_queryset().cancelled()

    def by_customer(self, customer):
        return self.get_queryset().by_customer(customer)

    def by_status(self, status):
        return self.get_queryset().by_status(status)


class OrderItemQuerySet(models.QuerySet):

    def by_order(self, order):
        return self.filter(order=order)

    def by_product(self, product):
        return self.filter(product=product)


class OrderItemManager(models.Manager):

    def get_queryset(self):
        return OrderItemQuerySet(self.model, using=self._db)

    def by_order(self, order):
        return self.get_queryset().by_order(order)

    def by_product(self, product):
        return self.get_queryset().by_product(product)

