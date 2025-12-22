from decimal import Decimal

from rest_framework import serializers
from products.models import Product
from products.services import ProductService


class ProductListSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    sku = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    category = serializers.CharField(read_only=True)
    cost_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    selling_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    stock_qty = serializers.IntegerField(read_only=True)
    image = serializers.ImageField(read_only=True, allow_null=True)
    stock_status = serializers.CharField()
    profit_margin = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    modified_at = serializers.DateTimeField(read_only=True)
    created_by = serializers.IntegerField(source='created_by.full_name', read_only=True)
    modified_by = serializers.IntegerField(source='modified_by.full_name', read_only=True)

def validate_product_prices(selling_price, cost_price):
    if selling_price < cost_price:
        raise serializers.ValidationError("Selling price should not be less than cost price.")

class ProductCreateSerializer(serializers.Serializer):

    sku = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=255)
    category = serializers.CharField(max_length=100)
    cost_price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal(0.01))
    selling_price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal(0.01))
    stock_qty = serializers.IntegerField(min_value=0)
    image = serializers.ImageField(required=False, allow_null=True)

    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    modified_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_sku(self, value):
        value = value.upper().strip()

        if not value.replace('-', '').replace('_', '').isalnum():
            raise serializers.ValidationError(
                "SKU must contain only alphanumeric characters, hyphens, and underscores."
            )

        if Product.objects.filter(sku=value).exists():
            raise serializers.ValidationError("Product with this SKU already exists.")

        return value


    def validate(self, attrs):
        validate_product_prices(attrs['selling_price'], attrs['cost_price'])
        return attrs

    def create(self, validated_data):
        return ProductService.create_new_product(**validated_data)


class ProductRetrieveSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    sku = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    category = serializers.CharField(read_only=True)
    cost_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    selling_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    stock_qty = serializers.IntegerField(read_only=True)
    image = serializers.ImageField(read_only=True, allow_null=True)
    profit_margin = serializers.CharField(read_only=True)
    stock_status = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    modified_at = serializers.DateTimeField(read_only=True)
    created_by= serializers.CharField(source='created_by.get_full_name')
    modified_by= serializers.CharField(source='modified_by.get_full_name')



class ProductUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=False)
    category = serializers.CharField(max_length=100, required=False)
    cost_price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal(0.01), required=False)
    selling_price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal(0.01), required=False)
    stock_qty = serializers.IntegerField(min_value=0, required=False)
    image = serializers.ImageField(required=False, allow_null=True)

    def validate(self, attrs):
        validate_product_prices(attrs['selling_price'], attrs['cost_price'])
        return attrs

    def update(self, instance, validated_data):
        user = self.context['request'].user
        return ProductService.update_product(instance, validated_data, user)



class StockChangeLogListSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    product_id = serializers.IntegerField(read_only=True)
    product_name = serializers.CharField(read_only=True)
    product_category = serializers.CharField(read_only=True)
    product_sku = serializers.CharField(read_only=True)


    previous_qty = serializers.IntegerField(read_only=True)
    new_qty = serializers.IntegerField(read_only=True)
    quantity_change = serializers.IntegerField()
    change_reason = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    created_by = serializers.CharField(source='created_by.get_full_name', read_only=True)
    customer = serializers.CharField(source='customer.get_full_name',read_only=True,allow_null=True)




