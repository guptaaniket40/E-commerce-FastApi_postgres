from fastapi import HTTPException, status

from src.services.orders.schema import OrderSchema
from src.services.orders.serializers import OrderResponse
from src.utils.response import success_response


class OrderController:

    @classmethod
    async def checkout(cls, current_user):
        cart_items = await OrderSchema.get_user_cart(
            user_id=current_user.id
        )

        if not cart_items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cart is empty"
            )

        total_amount = 0

        for item in cart_items:
            total_amount += item.quantity * item.product.price

        new_order = await OrderSchema.create_order(
            user_id=current_user.id,
            total_amount=total_amount
        )

        items_data = []

        for item in cart_items:
            await OrderSchema.create_order_item(
                order_id=new_order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.product.price
            )

            items_data.append({
                "product_id": item.product_id,
                "product_name": item.product.name,
                "quantity": item.quantity,
                "price": item.product.price,
                "total": item.quantity * item.product.price
            })

        payment = await OrderSchema.create_payment(
            order_id=new_order.id,
            amount=total_amount
        )

        await OrderSchema.delete_cart_items(
            cart_items=cart_items
        )

        return success_response(
    "Order placed successfully",
    {
        "order_id": new_order.id,
        "total_amount": new_order.total_amount,
        "order_status": new_order.status,
        "payment_status": payment.status,
        "payment_method": payment.payment_method,
        "transaction_id": payment.transaction_id,
         
    }
)

    @classmethod
    async def get_my_orders(cls, current_user):
        orders = await OrderSchema.get_order_data(
            user_id=current_user.id
        )

        return success_response(
            "Orders fetched successfully",
            [
                OrderResponse.model_validate(order).model_dump(mode="json")
                for order in orders
            ]
        )

    @classmethod
    async def get_order_detail(cls, order_id, current_user):
        order = await OrderSchema.get_order_data(
            user_id=current_user.id,
            order_id=order_id
        )

        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )

        items_data = []

        for item in order.items:
            items_data.append({
                "product_id": item.product_id,
                "product_name": item.product.name,
                "quantity": item.quantity,
                "price": item.price,
                "total": item.quantity * item.price
            })

        payment_data = None

        if order.payment:
            payment_data = {
                "amount": order.payment.amount,
                "status": order.payment.status,
                "payment_method": order.payment.payment_method,
                "transaction_id": order.payment.transaction_id
            }

        return success_response(
            "Order fetched successfully",
            {
                "order": OrderResponse.model_validate(order).model_dump(mode="json"),
                "items": items_data,
                "payment": payment_data
            }
        )