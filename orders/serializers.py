from decimal import Decimal
from rest_framework import serializers

from orders.constants import ORDER_STATUS_CHOICES, ORDER_STATUS_CONFIRMED, ORDER_STATUS_PENDING, ORDER_STATUS_CANCELLED
from orders.services import OrderService
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
    modified_at = serializers.DateTimeField(read_only=True)
    modified_by = serializers.CharField(source='modified_by.get_full_name', read_only=True)


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

        product_ids = [item_data['product_id'] for item_data in items]

        if len(product_ids) != len(set(product_ids)):
            raise serializers.ValidationError({
                'items': "Duplicate product IDs found in order items."
            })

        products = Product.objects.filter(id__in=product_ids)
        products_dict = {product.id: product for product in products}

        missing_ids = set(product_ids) - set(products_dict.keys())
        if missing_ids:
            raise serializers.ValidationError({
                'items': f"Products with IDs {list(missing_ids)} not found."
            })

        stock_errors = []
        for item_data in items:
            product_id = item_data['product_id']
            quantity = item_data['quantity']
            product = products_dict[product_id]

            if product.stock_qty < quantity:
                stock_errors.append(
                    f"{product.name} sku: {product.sku}"
                )

        if stock_errors:
            raise serializers.ValidationError({
                'items': f"Insufficient stock for: {'; '.join(stock_errors)}"
            })

        attrs['products_dict'] = products_dict
        return attrs

    def create(self, validated_data):
        return OrderService.create_order(**validated_data)


class OrderRetrieveSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    order_number = serializers.CharField(read_only=True)
    customer_id = serializers.IntegerField(source='customer.id', read_only=True)
    customer = serializers.CharField(source='get_full_name', read_only=True)
    order_date = serializers.DateField(read_only=True)
    status = serializers.CharField(read_only=True)
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    items = OrderItemDetailSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    modified_at = serializers.DateTimeField(read_only=True)
    created_by = serializers.CharField(source='created_by.get_full_name', read_only=True)
    modified_by = serializers.CharField(source='modified_by.get_full_name', read_only=True)


class OrderStatusUpdateSerializer(serializers.Serializer):

    status = serializers.ChoiceField(
        choices=ORDER_STATUS_CHOICES,
    )

    def validate(self, attrs):
        instance = self.instance
        new_status = attrs.get('status')

        if not new_status:
            raise serializers.ValidationError({'status': "This field is required."})

        if new_status == instance.status:
            raise serializers.ValidationError("Status is already set to the specified value.")

        if instance.status == ORDER_STATUS_CONFIRMED and new_status == ORDER_STATUS_PENDING:
            raise serializers.ValidationError("Cannot change status from CONFIRMED to PENDING.")

        if instance.status == ORDER_STATUS_CANCELLED:
            raise serializers.ValidationError("Cannot change status of a cancelled order.")

        return attrs

    def update(self, instance, validated_data):

        user = self.context['request'].user
        new_status = validated_data.get('status')

        return OrderService.change_order_status(
            order=instance,
            new_status=new_status,
            user=user
        )


