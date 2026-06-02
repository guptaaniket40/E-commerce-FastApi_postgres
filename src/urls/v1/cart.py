from fastapi import APIRouter, Depends

from src.services.cart.controller import CartController
from src.services.cart.serializers import AddCartItem, UpdateCartItem
from src.utils.security import get_current_user


router = APIRouter(prefix="/cart",tags=["Cart"])


@router.post("/")
async def add_to_cart(
    request: AddCartItem,
    current_user=Depends(get_current_user)
):
    return await CartController.add_to_cart(
        request,
        current_user
    )


@router.get("/")
async def get_cart(
    current_user=Depends(get_current_user)
):
    return await CartController.get_cart(
        current_user
    )

@router.get("/{cart_item_id}")
async def get_cart_item(
    cart_item_id:int,
    current_user=Depends(
        get_current_user
    )
):

    return await CartController.get_cart_item(

        cart_item_id,

        current_user
    )

@router.patch("/{cart_item_id}")
async def update_cart(
    cart_item_id: int,
    request: UpdateCartItem,
    current_user=Depends(get_current_user)
):
    return await CartController.update_cart(
        cart_item_id,
        request,
        current_user
    )


@router.delete("/{cart_item_id}")
async def remove_cart_item(
    cart_item_id: int,
    current_user=Depends(get_current_user)
):
    return await CartController.delete_cart_item(
        cart_item_id,
        current_user
    )