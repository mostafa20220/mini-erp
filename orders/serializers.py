from decimal import Decimal
from rest_framework import serializers
from orders.services import OrderService, OrderStatusService
from users.models import User
from users.constants import ROLE_CUSTOMER
from products.models import Product


class OrderItemSerializer(serializers.Serializer):

    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal('0.01'), required=False)


class OrderItemDetailSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    product_id = serializers.IntegerField(read_only=True)
    product_name = serializers.CharField(read_only=True)
    product_sku = serializers.CharField(read_only=True)
    quantity = serializers.IntegerField(read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)


class OrderListSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    order_number = serializers.CharField(read_only=True)
    customer_id = serializers.IntegerField(read_only=True)
    customer = serializers.CharField(source='get_full_name', read_only=True)
    order_date = serializers.DateField(read_only=True)
    status = serializers.CharField(read_only=True)
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    created_by = serializers.CharField(source='created_by.get_full_name', read_only=True)


class OrderCreateSerializer(serializers.Serializer):

    customer_id = serializers.IntegerField()
    items = OrderItemSerializer(many=True,allow_empty=False)
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    modified_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_customer_id(self, value):
        if not User.objects.filter(id=value, role=ROLE_CUSTOMER).exists():
            raise serializers.ValidationError("Customer not found or not a valid customer.")
        return value

    def validate(self, attrs):

        items = attrs.get('items')

        for item_data in items:
            product_id = item_data['product_id']
            quantity = item_data['quantity']

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                raise serializers.ValidationError({
                    'items': f"Product with ID {product_id} not found."
                })

            if product.stock_qty < quantity:
                raise serializers.ValidationError({
                    'items': f"Insufficient stock for {product.name}. Available: {product.stock_qty}, Requested: {quantity}"
                })

        return attrs

    def create(self, validated_data):
        return OrderService.create_order(**validated_data)


class OrderRetrieveSerializer(serializers.Serializer):
    """Serializer for retrieving a single order (GET /api/v1/orders/{id}/)."""

    id = serializers.IntegerField(read_only=True)
    order_number = serializers.CharField(read_only=True)
    customer_id = serializers.IntegerField(source='customer.id', read_only=True)
    customer_details = serializers.SerializerMethodField()
    order_date = serializers.DateField(read_only=True)
    status = serializers.CharField(read_only=True)
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    items = OrderItemDetailSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    modified_at = serializers.DateTimeField(read_only=True)
    created_by = serializers.CharField(source='created_by.get_full_name', read_only=True)
    modified_by = serializers.CharField(source='modified_by.get_full_name', read_only=True)

    def get_customer_details(self, obj):
        """Get customer information."""
        return {
            'id': obj.customer.id,
            'email': obj.customer.email,
            'name': obj.customer.get_full_name() or obj.customer.email,
        }


class OrderUpdateSerializer(serializers.Serializer):
    """Serializer for updating orders (PUT/PATCH /api/v1/orders/{id}/)."""

    status = serializers.ChoiceField(
        choices=['PENDING', 'CONFIRMED', 'CANCELLED'],
        required=False
    )

    def validate_status(self, value):
        """Validate status transition."""
        instance = self.instance

        if not instance:
            return value

        # Validate status transitions
        if instance.status == 'CONFIRMED' and value == 'PENDING':
            raise serializers.ValidationError("Cannot change status from CONFIRMED to PENDING.")

        if instance.status == 'CANCELLED':
            raise serializers.ValidationError("Cannot change status of a cancelled order.")

        return value

    def update(self, instance, validated_data):
        """Update order using service layer."""
        user = self.context['request'].user
        new_status = validated_data.get('status')

        if new_status and new_status != instance.status:
            # Use status service to handle transitions and stock management
            return OrderStatusService.change_order_status(
                order=instance,
                new_status=new_status,
                user=user
            )

        return instance

