from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from orders.models import Order, OrderItem
from orders.serializers import (
    OrderListSerializer,
    OrderCreateSerializer,
    OrderRetrieveSerializer,
    OrderUpdateSerializer,
    OrderItemDetailSerializer
)
from orders.filters import OrderFilter, OrderItemFilter
from orders.services import OrderService
from users.permissions import IsSales, IsAdmin


class ListCreateOrdersApiView(ListCreateAPIView):

    queryset = Order.objects.all()
    permission_classes = [IsSales | IsAdmin]
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['order_number', 'customer__email', 'customer__first_name', 'customer__last_name']
    ordering_fields = ['id', 'order_number', 'order_date', 'total_amount', 'status', 'created_at']
    ordering = ['-id']

    def get_serializer_class(self):

        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderListSerializer

    def get_queryset(self):
        return Order.objects.select_related('customer', 'created_by').all()


class RetrieveUpdateDestroyOrderApiView(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return OrderUpdateSerializer
        return OrderRetrieveSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsSales | IsAdmin]
        else:
            self.permission_classes = [IsAdmin]
        return super().get_permissions()

    def get_queryset(self):
        return Order.objects.select_related(
            'customer', 'created_by', 'modified_by'
        ).prefetch_related(
            'items__product'
        ).all()

    def perform_destroy(self, instance):
        OrderService.delete_order(instance)


class OrderItemsListApiView(ListAPIView):

    serializer_class = OrderItemDetailSerializer
    permission_classes = [IsSales | IsAdmin]
    filterset_class = OrderItemFilter
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering = ['id']


    def get_queryset(self):
        order_id = self.kwargs.get('order_id')
        return OrderItem.objects.filter(
            order_id=order_id
        ).select_related('product', 'order').all()
