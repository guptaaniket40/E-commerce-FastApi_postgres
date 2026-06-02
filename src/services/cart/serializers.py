from typing import Annotated

from pydantic import BaseModel, Field


class AddCartItem(BaseModel):
    product_id: int
    quantity: Annotated[int, Field(gt=0)] = 1


class UpdateCartItem(BaseModel):
    quantity: Annotated[int, Field(gt=0)]