from django.db import transaction
from datetime import datetime

from orders.constants import ORDER_STATUS_CANCELLED, ORDER_STATUS_CONFIRMED, ORDER_STATUS_PENDING
from users.models import User
from orders.models import Order, OrderItem
from products.services import ProductStockService
from products.models import Product


class OrderNumberService:

    @staticmethod
    def generate_order_number():
        today = datetime.now().strftime('%Y%m%d')
        prefix = f"ORD-{today}"

        last_order = Order.objects.filter(
            order_number__startswith=prefix
        ).order_by('-order_number').first()

        if last_order:
            last_sequence = int(last_order.order_number.split('-')[-1])
            new_sequence = last_sequence + 1
        else:
            new_sequence = 1

        order_number = f"{prefix}-{new_sequence:04d}"

        return order_number


class OrderService:

    @staticmethod
    @transaction.atomic
    def create_order(customer_id, items, created_by, modified_by):

        customer = User.objects.get(id=customer_id)
        order_number = OrderNumberService.generate_order_number()

        order = Order.objects.create(
            order_number=order_number,
            customer=customer,
            status=ORDER_STATUS_PENDING,
            total_amount=0.00,
            created_by=created_by,
            modified_by=modified_by
        )

        total_amount = 0
        for item_data in items:
            product = Product.objects.get(id=item_data['product_id'])

            price = item_data.get('price', product.selling_price)
            quantity = item_data['quantity']

            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                product_sku=product.sku,
                quantity=quantity,
                price=price,
                total_price=quantity * price
            )

            total_amount += quantity * price

        order.total_amount = total_amount
        order.save(update_fields=['total_amount'])

        return order

    @staticmethod
    @transaction.atomic
    def update_order(instance, validated_data, user):
        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.modified_by = user
        instance.save()

        return instance

    @staticmethod
    @transaction.atomic
    def delete_order(instance, user):
        if instance.status != ORDER_STATUS_PENDING:
            raise ValueError("Only pending orders can be deleted.")

        instance.delete()


class OrderStatusService:

    @staticmethod
    @transaction.atomic
    def change_order_status(order, new_status, user):
        old_status = order.status

        if old_status == new_status:
            return order

        # Handle status transitions
        if new_status == ORDER_STATUS_CONFIRMED:
            OrderStatusService._confirm_order(order, user)
        elif new_status == ORDER_STATUS_CANCELLED:
            OrderStatusService._cancel_order(order, old_status, user)

        order.status = new_status
        order.modified_by = user
        order.save(update_fields=['status', 'modified_by', 'modified_at'])

        return order

    @staticmethod
    def _confirm_order(order, user):
        if order.status != ORDER_STATUS_PENDING:
            raise ValueError("Only pending orders can be confirmed.")

        for item in order.items.all():
            success, message = ProductStockService.decrease_stock(
                product=item.product,
                quantity=item.quantity,
                customer=order.customer,
                sales_user=user,
                reason=f"Order {order.order_number} confirmed"
            )

            if not success:
                raise ValueError(f"Failed to decrease stock for {item.product_name}: {message}")

    @staticmethod
    def _cancel_order(order, old_status, user):

        if old_status == ORDER_STATUS_CONFIRMED:
            for item in order.items.all():
                success, message = ProductStockService.increase_stock(
                    product=item.product,
                    quantity=item.quantity,
                    customer=order.customer,
                    sales_user=user,
                    reason=f"Order {order.order_number} cancelled"
                )

                if not success:
                    raise ValueError(f"Failed to return stock for {item.product_name}: {message}")

