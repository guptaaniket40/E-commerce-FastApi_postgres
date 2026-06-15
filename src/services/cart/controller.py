from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.database.models import Product
from src.services.cart.schema import CartSchema
from src.utils.response import success_response


class CartController:

    @classmethod
    async def add_to_cart(cls, cart_data, current_user, db: AsyncSession):

        result = await db.execute(
            select(Product).where(Product.id == cart_data.product_id)
        )
        product = result.scalar_one_or_none()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        existing_item = await CartSchema.get_cart_item(
            db=db,
            user_id=current_user.id,
            product_id=product.id
        )

        if existing_item:
            existing_item.quantity += cart_data.quantity
            await db.commit()
            await db.refresh(existing_item)

            return success_response("Cart updated successfully", {
                "cart_item_id": existing_item.id,
                "product_id": product.id,
                "product_name": product.name,
                "quantity": existing_item.quantity,
                "price": product.price,
                "total": existing_item.quantity * product.price
            })

        cart_item = await CartSchema.create_cart_item(
            db=db,
            user_id=current_user.id,
            product_id=product.id,
            quantity=cart_data.quantity
        )

        return success_response("Product added to cart", {
            "cart_item_id": cart_item.id,
            "product_id": product.id,
            "product_name": product.name,
            "quantity": cart_item.quantity,
            "price": product.price,
            "total": cart_item.quantity * product.price
        })

    @classmethod
    async def get_cart(cls, current_user, db: AsyncSession):

        items = await CartSchema.get_cart_data(db=db, user_id=current_user.id)

        data = [
            {
                "cart_item_id": item.id,
                "product_id": item.product.id,
                "product_name": item.product.name,
                "quantity": item.quantity,
                "price": item.product.price,
                "total": item.quantity * item.product.price
            }
            for item in items
        ]

        return success_response("Cart fetched successfully", data)

    @classmethod
    async def delete_cart_item(cls, cart_item_id, current_user, db: AsyncSession):

        item = await CartSchema.get_cart_item_by_id(
            db=db,
            cart_item_id=cart_item_id,
            user_id=current_user.id
        )

        if not item:
            raise HTTPException(status_code=404, detail="Cart item not found")

        await CartSchema.delete_cart_item(db=db, cart_item=item)

        return success_response("Cart item removed")