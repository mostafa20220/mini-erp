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

        # Log initial stock
        ProductService._log_stock_change(
            product=product,
            previous_qty=0,
            new_qty=stock_qty,
            created_by=created_by,
            reason="Initial stock on product creation"
        )

        return product

    @staticmethod
    @transaction.atomic
    def update_product(instance: Product, validated_data: dict, user) -> Product:
        old_stock_qty = instance.stock_qty
        new_stock_qty = validated_data.get('stock_qty', old_stock_qty)

        # Update fields
        instance.modified_by = user
        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()

        # Handle stock change if stock quantity changed
        if old_stock_qty != new_stock_qty:
            ProductService.update_stock(
                product=instance,
                new_qty=new_stock_qty,
                user=user,
                reason=f"Stock updated by {user.get_full_name()}"
            )

        return instance

    @staticmethod
    @transaction.atomic
    def delete_product(instance: Product, user) -> None:
        if instance.stock_qty > 0:
            ProductService._log_stock_change(
                product=instance,
                previous_qty=instance.stock_qty,
                new_qty=0,
                created_by=user,
                reason=f"Product deleted by {user.get_full_name()}"
            )

        instance.delete()

    @staticmethod
    @transaction.atomic
    def update_stock(
        product: Product,
        new_qty: int,
        user,
        customer=None,
        reason: str = "Stock adjustment"
    ) -> StockChangeLog:

        # Lock the product row to prevent race conditions
        product = Product.objects.select_for_update().get(pk=product.pk)

        previous_qty = product.stock_qty

        # Update stock
        product.stock_qty = new_qty
        product.save(update_fields=['stock_qty', 'modified_at'])

        # Log stock change
        return ProductService._log_stock_change(
            product=product,
            previous_qty=previous_qty,
            new_qty=new_qty,
            created_by=user,
            customer=customer,
            reason=reason
        )

    @staticmethod
    def _log_stock_change(
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


