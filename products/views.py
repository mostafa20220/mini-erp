from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from products.models import Product, StockChangeLog
from products.serializers import (
    ProductListSerializer,
    ProductCreateSerializer,
    ProductRetrieveSerializer,
    ProductUpdateSerializer,
    StockChangeLogListSerializer
)
from products.filters import ProductFilter, StockChangeLogFilter
from products.services import ProductService
from users.permissions import IsSales, IsAdmin


class ListCreateProductsApiView(ListCreateAPIView):

    queryset = Product.objects.all()
    filterset_class = ProductFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['sku', 'name', 'category']
    ordering_fields = ['id', 'sku', 'name', 'category', 'stock_qty', 'selling_price', 'created_at']
    ordering = ['-id']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductCreateSerializer
        return ProductListSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsSales | IsAdmin]
        else:
            self.permission_classes = [IsAdmin]
        return super().get_permissions()

class RetrieveUpdateDestroyProductApiView(RetrieveUpdateDestroyAPIView):

    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProductUpdateSerializer
        return ProductRetrieveSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsSales | IsAdmin]
        else:
            self.permission_classes = [IsAdmin]
        return super().get_permissions()

    def perform_destroy(self, instance):
        ProductService.delete_product(instance, self.request.user)

class ProductStockHistoryApiView(ListAPIView):

    serializer_class = StockChangeLogListSerializer
    permission_classes = [IsSales | IsAdmin]
    filterset_class = StockChangeLogFilter
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['id', 'created_at']
    ordering = ['-id']

    def get_queryset(self):
        return StockChangeLog.objects.select_related(
            'customer', 'created_by'
        ).all()



