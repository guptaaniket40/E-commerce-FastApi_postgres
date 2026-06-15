from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Product


class ProductSchema:

   
    @classmethod
    async def get_product_data(
        cls,
        db: AsyncSession,
        product_id=None
    ):
        query = select(Product)

        if product_id:
            query = query.where(Product.id == product_id)

        result = await db.execute(query)

        if product_id:
            return result.scalar_one_or_none()

        return result.scalars().all()
 
    @classmethod
    async def create_product(
        cls,
        db: AsyncSession,
        request,
        image_url=None
    ):
        product = Product(
            name=request.name,
            description=request.description,
            price=request.price,
            image_url=image_url
        )

        db.add(product)
        await db.commit()
        await db.refresh(product)

        return product

   
    @classmethod
    async def update_product(
        cls,
        db: AsyncSession,
        product,
        request,
        image_url=None
    ):
        update_data = request.model_dump(
            exclude_unset=True,
            exclude={"image_base64", "image_name"}
        )

        for key, value in update_data.items():
            setattr(product, key, value)

        if image_url:
            product.image_url = image_url

        await db.commit()
        await db.refresh(product)

        return product
 
    @classmethod
    async def delete_product(
        cls,
        db: AsyncSession,
        product
    ):
        await db.delete(product)
        await db.commit()
        return True