from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.database.models import CartItem


class CartSchema:

    @classmethod
    async def get_cart_item(cls, db, user_id, product_id):
        result = await db.execute(
            select(CartItem).where(
                CartItem.user_id == user_id,
                CartItem.product_id == product_id
            )
        )
        return result.scalar_one_or_none()

    @classmethod
    async def get_cart_data(cls, db, user_id):

        result = await db.execute(
            select(CartItem)
            .options(selectinload(CartItem.product))
            .where(CartItem.user_id == user_id)
        )

        return result.scalars().all()

    @classmethod
    async def create_cart_item(cls, db, user_id, product_id, quantity):

        cart_item = CartItem(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity
        )

        db.add(cart_item)
        await db.commit()
        await db.refresh(cart_item)

        return cart_item

    @classmethod
    async def get_cart_item_by_id(cls, db, cart_item_id, user_id):

        result = await db.execute(
            select(CartItem)
            .options(selectinload(CartItem.product))
            .where(
                CartItem.id == cart_item_id,
                CartItem.user_id == user_id
            )
        )

        return result.scalar_one_or_none()

    @classmethod
    async def update_cart_item(cls, db, cart_item, quantity):

        cart_item.quantity = quantity
        await db.commit()
        await db.refresh(cart_item)

        return cart_item

    @classmethod
    async def delete_cart_item(cls, db, cart_item):

        await db.delete(cart_item)
        await db.commit()