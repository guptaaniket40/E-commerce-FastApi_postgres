from fastapi import HTTPException, status

from src.services.products.schema import ProductSchema
from src.services.products.serializers import ProductResponse
from src.utils.response import success_response
from src.utils.s3_upload import (
    upload_base64_image_to_s3,
    delete_image_from_s3
)


class ProductController:

    @classmethod
    async def create_product(
        cls,
        product_data
    ):
        image_url = None

        if product_data.image_base64 and product_data.image_name:
            image_url = await upload_base64_image_to_s3(
                image_base64=product_data.image_base64,
                image_name=product_data.image_name
            )

        new_product = await ProductSchema.create_product(
            request=product_data,
            image_url=image_url
        )

        return success_response(
            "Product created successfully",
            ProductResponse.model_validate(
                new_product
            ).model_dump(
                mode="json"
            )
        )

    @classmethod
    async def get_all_products(
        cls
    ):
        products = await ProductSchema.get_product_data()

        return success_response(
            "Products fetched successfully",
            [
                ProductResponse.model_validate(
                    product
                ).model_dump(
                    mode="json"
                )
                for product in products
            ]
        )

    @classmethod
    async def get_product_detail(
        cls,
        product_id: int
    ):
        product = await ProductSchema.get_product_data(
            product_id=product_id
        )

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        return success_response(
            "Product fetched successfully",
            ProductResponse.model_validate(
                product
            ).model_dump(
                mode="json"
            )
        )

    @classmethod
    async def update_product(
        cls,
        product_id: int,
        product_data
    ):
        product = await ProductSchema.get_product_data(
            product_id=product_id
        )

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        image_url = None

        if product_data.image_base64 and product_data.image_name:
            if product.image_url:
                await delete_image_from_s3(
                    product.image_url
                )

            image_url = await upload_base64_image_to_s3(
                image_base64=product_data.image_base64,
                image_name=product_data.image_name
            )

        updated_product = await ProductSchema.update_product(
            product=product,
            request=product_data,
            image_url=image_url
        )

        return success_response(
            "Product updated successfully",
            ProductResponse.model_validate(
                updated_product
            ).model_dump(
                mode="json"
            )
        )

    @classmethod
    async def delete_product(
        cls,
        product_id: int
    ):
        product = await ProductSchema.get_product_data(
            product_id=product_id
        )

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        if product.image_url:
            await delete_image_from_s3(
                product.image_url
            )

        await ProductSchema.delete_product(
            product=product
        )

        return success_response(
            "Product deleted successfully"
        )