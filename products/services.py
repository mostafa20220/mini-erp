from django.db import transaction
from products.models import Product, StockChangeLog


class ProductService:

    @staticmethod
    @transaction.atomic
    def create_new_product(
        sku: str,
        name: str,
        category: str,
        cost_price: float,
        selling_price: float,
        stock_qty: int,
        image,
        created_by,
        modified_by
    ) -> Product:

        product = Product.objects.create(
            sku=sku,
            name=name,
            category=category,
            cost_price=cost_price,
            selling_price=selling_price,
            stock_qty=stock_qty,
            image=image,
            created_by=created_by,
            modified_by=modified_by
        )

        ProductStockService.log_stock_change(
            product=product,
            previous_qty=0,
            new_qty=stock_qty,
            created_by=created_by,
            reason="Initial stock on product creation"
        )

        return product

    @staticmethod
    def update_product(instance: Product, validated_data: dict, user) -> Product:
        old_stock_qty = instance.stock_qty
        new_stock_qty = validated_data.get('stock_qty', old_stock_qty)

        # Update fields
        instance.modified_by = user
        for field, value in validated_data.items():
            setattr(instance, field, value)


        with transaction.atomic():
            instance.save()

            if old_stock_qty != new_stock_qty:
                ProductStockService.log_stock_change(
                    product=instance,
                    previous_qty=old_stock_qty,
                    new_qty=new_stock_qty,
                    created_by=user,
                    reason=f"Stock updated by {user.get_full_name() or user.email}"
                )

        return instance

    @staticmethod
    @transaction.atomic
    def delete_product(instance: Product, user) -> None:
        if instance.stock_qty > 0:
            ProductStockService.log_stock_change(
                product=instance,
                previous_qty=instance.stock_qty,
                new_qty=0,
                created_by=user,
                reason=f"Product deleted by {user.get_full_name()}"
            )

        instance.delete()



class ProductStockService:

    @staticmethod
    def log_stock_change(
        product: Product,
        previous_qty: int,
        new_qty: int,
        created_by,
        customer=None,
        reason: str = "Stock change"
    ) -> StockChangeLog:

        return StockChangeLog.objects.create(
            product=product,
            product_name=product.name,
            product_category=product.category,
            product_sku=product.sku,
            customer=customer,
            previous_qty=previous_qty,
            new_qty=new_qty,
            change_reason=reason,
            created_by=created_by
        )

    @staticmethod
    @transaction.atomic
    def decrease_stock(
        product: Product,
        quantity: int,
        customer,
        sales_user=None,
        reason: str = "Sales order"
    ) :

        if quantity <= 0:
            return False, "Quantity must be greater than 0"

        product = Product.objects.select_for_update().get(pk=product.pk)

        if product.stock_qty < quantity:
            return False, f"Insufficient stock. Available: {product.stock_qty}, Required: {quantity}"

        # Store previous quantity for logging
        previous_qty = product.stock_qty

        # Decrease stock
        product.stock_qty -= quantity
        product.save(update_fields=['stock_qty', 'modified_at'])

        # Log stock change
        return ProductStockService.log_stock_change(
            product=product,
            previous_qty=previous_qty,
            new_qty=product.stock_qty,
            created_by=sales_user or customer,
            customer=customer,
            reason=reason
        )


    @staticmethod
    @transaction.atomic
    def increase_stock(
        product: Product,
        quantity: int,
        customer=None,
        sales_user=None,
        reason: str = "Stock adjustment"
    ):

        if quantity <= 0:
            return False, "Quantity must be greater than 0"

        # Lock the product row
        product = Product.objects.select_for_update().get(pk=product.pk)

        previous_qty = product.stock_qty

        # Increase stock
        product.stock_qty += quantity
        product.save(update_fields=['stock_qty', 'modified_at'])

        # Log stock change
        return ProductStockService.log_stock_change(
            product=product,
            previous_qty=previous_qty,
            new_qty=product.stock_qty,
            created_by=sales_user or customer,
            customer=customer,
            reason=reason
        )

