from django.db import models
from products.constants import LOW_STOCK_THRESHOLD


class ProductQuerySet(models.QuerySet):

    def in_stock(self):
        return self.filter(stock_qty__gt=0)

    def out_of_stock(self):
        return self.filter(stock_qty=0)

    def low_stock(self, threshold=LOW_STOCK_THRESHOLD):
        return self.filter(stock_qty__lte=threshold, stock_qty__gt=0)

    def by_category(self, category):
        if category:
            return self.filter(category__iexact=category)
        return self


class ProductManager(models.Manager):

    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def in_stock(self):
        return self.get_queryset().in_stock()

    def out_of_stock(self):
        return self.get_queryset().out_of_stock()

    def low_stock(self, threshold=LOW_STOCK_THRESHOLD):
        return self.get_queryset().low_stock(threshold)

