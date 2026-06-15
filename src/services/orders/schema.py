import uuid
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import CartItem, Order, OrderItem, Payment


class OrderSchema:
 
    @classmethod
    async def get_user_cart(cls, db: AsyncSession, user_id):
        result = await db.execute(
            select(CartItem)
            .options(selectinload(CartItem.product))
            .where(CartItem.user_id == user_id)
        )
        return result.scalars().all()

     
    @classmethod
    async def create_order(cls, db: AsyncSession, user_id, total_amount):
        order = Order(
            user_id=user_id,
            total_amount=total_amount,
            status="confirmed"
        )

        db.add(order)
        await db.commit()
        await db.refresh(order)
        return order

     
    @classmethod
    async def create_order_item(cls, db: AsyncSession, order_id, product_id, quantity, price):
        item = OrderItem(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            price=price
        )

        db.add(item)
        await db.commit()
        await db.refresh(item)
        return item

    
    @classmethod
    async def create_payment(cls, db: AsyncSession, order_id, amount):
        payment = Payment(
            order_id=order_id,
            amount=amount,
            status="success",
            payment_method="dummy",
            transaction_id=str(uuid.uuid4())
        )

        db.add(payment)
        await db.commit()
        await db.refresh(payment)
        return payment

   
    @classmethod
    async def delete_cart_items(cls, db: AsyncSession, cart_items):
        for item in cart_items:
            await db.delete(item)

        await db.commit()

   
    @classmethod
    async def get_order_data(cls, db: AsyncSession, user_id, order_id=None):
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