from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.products.schema import ProductSchema
from src.database.models import CartItem, OrderItem
from src.services.products.serializers import ProductResponse
from src.utils.response import success_response
from src.utils.s3_upload import upload_base64_image_to_s3, delete_image_from_s3


class ProductController:

 
    @classmethod
    async def create_product(cls, db: AsyncSession, product_data):

        image_url = None

        if product_data.image_base64 and product_data.image_name:
            image_url = await upload_base64_image_to_s3(
                image_base64=product_data.image_base64,
                image_name=product_data.image_name
            )

        product = await ProductSchema.create_product(
            db=db,
            request=product_data,
            image_url=image_url
        )

        return success_response(
            "Product created successfully",
            ProductResponse.model_validate(product).model_dump(mode="json")
        )

   
    @classmethod
    async def get_all_products(cls, db: AsyncSession):

        products = await ProductSchema.get_product_data(db=db)

        return success_response(
            "Products fetched successfully",
            [
                ProductResponse.model_validate(p).model_dump(mode="json")
                for p in products
            ]
        )

    
    @classmethod
    async def get_product_detail(cls, db: AsyncSession, product_id: int):

        product = await ProductSchema.get_product_data(
            db=db,
            product_id=product_id
        )

        if not product:
            raise HTTPException(404, "Product not found")

        return success_response(
            "Product fetched successfully",
            ProductResponse.model_validate(product).model_dump(mode="json")
        )

    
    @classmethod
    async def update_product(cls, db: AsyncSession, product_id: int, product_data):

        product = await ProductSchema.get_product_data(
            db=db,
            product_id=product_id
        )

        if not product:
            raise HTTPException(404, "Product not found")

        image_url = product.image_url

        if product_data.image_base64 and product_data.image_name:

            # delete old image safely
            if product.image_url:
                await delete_image_from_s3(product.image_url)

            image_url = await upload_base64_image_to_s3(
                image_base64=product_data.image_base64,
                image_name=product_data.image_name
            )

        updated = await ProductSchema.update_product(
            db=db,
            product=product,
            request=product_data,
            image_url=image_url
        )

        return success_response(
            "Product updated successfully",
            ProductResponse.model_validate(updated).model_dump(mode="json")
        )

   
    @classmethod
    async def delete_product(cls, db: AsyncSession, product_id: int):

        product = await ProductSchema.get_product_data(
            db=db,
            product_id=product_id
        )

        if not product:
            raise HTTPException(404, "Product not found")
 
        order_exists = await db.execute(
            select(OrderItem.id).where(
                OrderItem.product_id == product.id
            ).limit(1)
        )

        if order_exists.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product already used in orders, cannot delete"
            )

    
        await db.execute(
            select(CartItem).where(
                CartItem.product_id == product.id
            )
        )

        cart_items = (await db.execute(
            select(CartItem).where(CartItem.product_id == product.id)
        )).scalars().all()

        for item in cart_items:
            await db.delete(item)

   
        if product.image_url:
            await delete_image_from_s3(product.image_url)

        await ProductSchema.delete_product(db=db, product=product)

        return success_response("Product deleted successfully")