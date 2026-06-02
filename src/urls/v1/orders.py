from fastapi import APIRouter, Depends

from src.services.orders.controller import OrderController
from src.utils.security import get_current_user


router = APIRouter(prefix="/orders",tags=["Orders"])


@router.post("/checkout")
async def checkout(
    current_user=Depends(get_current_user)
):
    return await OrderController.checkout(
        current_user=current_user
    )


@router.get("/")
async def get_my_orders(
    current_user=Depends(get_current_user)
):
    return await OrderController.get_my_orders(
        current_user=current_user
    )


@router.get("/{order_id}")
async def get_order_detail(
    order_id: int,
    current_user=Depends(get_current_user)
):
    return await OrderController.get_order_detail(
        order_id=order_id,
        current_user=current_user
    )