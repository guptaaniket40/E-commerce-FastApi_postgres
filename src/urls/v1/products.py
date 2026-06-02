from fastapi import APIRouter, Depends

from src.services.products.serializers import (
    ProductCreate,
    ProductUpdate
)

from src.services.products.controller import ProductController
from src.utils.security import get_current_user


router = APIRouter(prefix="/products",tags=["Products"])


@router.post("/")
async def create_product(
    request: ProductCreate,
    current_user = Depends(get_current_user)
):
    return await ProductController.create_product(
        product_data=request
    )


@router.get("/")
async def get_all_products():
    return await ProductController.get_all_products()


@router.get("/{product_id}")
async def get_product_detail(
    product_id: int
):
    return await ProductController.get_product_detail(
        product_id=product_id
    )


@router.patch("/{product_id}")
async def update_product(
    product_id: int,
    request: ProductUpdate,
    current_user = Depends(get_current_user)
):
    return await ProductController.update_product(
        product_id=product_id,
        product_data=request
    )


@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    current_user = Depends(get_current_user)
):
    return await ProductController.delete_product(
        product_id=product_id
    )