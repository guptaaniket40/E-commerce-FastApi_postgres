from fastapi import HTTPException, status

from sqlalchemy import select

from src.database.db_config import db
from src.database.models import Product
from src.services.cart.schema import CartSchema
from src.utils.response import success_response


class CartController:

    @classmethod
    async def add_to_cart(cls, cart_data, current_user):
        result = await db.execute(
            select(Product).where(
                Product.id == cart_data.product_id
            )
        )

        product = result.scalar_one_or_none()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        existing_item = await CartSchema.get_cart_item(
            current_user.id,
            product.id
        )

        if existing_item:
            existing_item.quantity += cart_data.quantity

            await db.commit()
            await db.refresh(existing_item)

            return success_response("Cart updated successfully")

        await CartSchema.create_cart_item(
            user_id=current_user.id,
            product_id=product.id,
            quantity=cart_data.quantity
        )

        return success_response("Product added to cart")

    @classmethod
    async def get_cart(cls, current_user):
        items = await CartSchema.get_cart_data(current_user.id)

        data = []

        for item in items:
            product = item.product

            data.append({
                "cart_item_id": item.id,
                "product_id": product.id,
                "product_name": product.name,
                "quantity": item.quantity,
                "price": product.price,
                "total": item.quantity * product.price
            })

        return success_response(
            "Cart fetched successfully",
            data
        )

    @classmethod
    async def get_cart_item(cls, cart_item_id, current_user):
        item = await CartSchema.get_cart_item_by_id(
            cart_item_id,
            current_user.id
        )

        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found"
            )

        product = item.product

        data = {
            "cart_item_id": item.id,
            "product_id": product.id,
            "product_name": product.name,
            "quantity": item.quantity,
            "price": product.price,
            "total": item.quantity * product.price
        }

        return success_response(
            "Cart item fetched successfully",
            data
        )

    @classmethod
    async def update_cart(cls, cart_item_id, cart_data, current_user):
        items = await CartSchema.get_cart_data(current_user.id)

        cart_item = next(
            (
                item for item in items
                if item.id == cart_item_id
            ),
            None
        )

        if not cart_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found"
            )

        await CartSchema.update_cart_item(
            cart_item,
            cart_data.quantity
        )

        return success_response("Cart updated successfully")

    @classmethod
    async def delete_cart_item(cls, cart_item_id, current_user):
        items = await CartSchema.get_cart_data(current_user.id)

        cart_item = next(
            (
                item for item in items
                if item.id == cart_item_id
            ),
            None
        )

        if not cart_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found"
            )

        await CartSchema.delete_cart_item(cart_item)

        return success_response("Cart item removed")