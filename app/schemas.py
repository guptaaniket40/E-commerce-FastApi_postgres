from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ProductCreate(BaseModel):
    name: str
    description: str
    price: int


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: int
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class AddToCartSchema(BaseModel):
    cart_id: int
    product_id: int
    quantity: int = 1


class CartCreateResponse(BaseModel):
    message: str
    cart_id: int


class CartItemView(BaseModel):
    item_id: int
    product_id: int
    product_name: str
    product_price: int
    quantity: int


class ViewCartResponse(BaseModel):
    cart_id: int
    items: List[CartItemView]


class CheckoutSchema(BaseModel):
    cart_id: int


class CheckoutResponse(BaseModel):
    order_id: int
    total: int
    payment: str