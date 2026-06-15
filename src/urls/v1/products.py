from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.products.serializers import (
    ProductCreate,
    ProductUpdate
)
from src.services.products.controller import ProductController
from src.utils.security import get_current_user
from src.database.db_config import get_db

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/")
async def create_product(
    request: ProductCreate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await ProductController.create_product(
        product_data=request,
        db=db
    )


@router.get("/")
async def get_all_products(
    db: AsyncSession = Depends(get_db)
):
    return await ProductController.get_all_products(db=db)


@router.get("/{product_id}")
async def get_product_detail(
    product_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await ProductController.get_product_detail(
        product_id=product_id,
        db=db
    )


@router.patch("/{product_id}")
async def update_product(
    product_id: int,
    request: ProductUpdate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await ProductController.update_product(
        product_id=product_id,
        product_data=request,
        db=db
    )


@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await ProductController.delete_product(
        product_id=product_id,
        db=db
    )