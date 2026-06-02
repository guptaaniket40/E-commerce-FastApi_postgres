import uuid

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.database.db_config import db
from src.database.models import CartItem, Order, OrderItem, Payment


class OrderSchema:

    @classmethod
    async def get_user_cart(cls, user_id):
        result = await db.execute(
            select(CartItem)
            .options(selectinload(CartItem.product))
            .where(CartItem.user_id == user_id)
        )

        return result.scalars().all()

    @classmethod
    async def create_order(cls, user_id, total_amount):
        new_order = Order(
            user_id=user_id,
            total_amount=total_amount,
            status="confirmed"
        )

        db.add(new_order)
        await db.commit()
        await db.refresh(new_order)

        return new_order

    @classmethod
    async def create_order_item(cls, order_id, product_id, quantity, price):
        new_order_item = OrderItem(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            price=price
        )

        db.add(new_order_item)
        await db.commit()
        await db.refresh(new_order_item)

        return new_order_item

    @classmethod
    async def create_payment(cls, order_id, amount):
        new_payment = Payment(
            order_id=order_id,
            amount=amount,
            status="success",
            payment_method="dummy",
            transaction_id=str(uuid.uuid4())
        )

        db.add(new_payment)
        await db.commit()
        await db.refresh(new_payment)

        return new_payment

    @classmethod
    async def delete_cart_items(cls, cart_items):
        for item in cart_items:
            await db.delete(item)

        await db.commit()

    @classmethod
    async def get_order_data(cls, user_id, order_id=None):
        query = select(Order).where(Order.user_id == user_id)

        if order_id:
            query = query.where(Order.id == order_id)

        query = query.options(
            selectinload(Order.items).selectinload(OrderItem.product),
            selectinload(Order.payment)
        )

        result = await db.execute(query)

        if order_id:
            return result.scalar_one_or_none()

        return result.scalars().all()