from typing import Annotated, Optional
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class ProductCreate(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=150)]
    description: Annotated[str, Field(min_length=5)]
    price: Annotated[float, Field(gt=0)]
    image_base64: Optional[str] = None
    image_name: Optional[str] = None


class ProductUpdate(BaseModel):
    name: Optional[Annotated[str, Field(min_length=2, max_length=150)]] = None
    description: Optional[Annotated[str, Field(min_length=5)]] = None
    price: Optional[Annotated[float, Field(gt=0)]] = None
    image_base64: Optional[str] = None
    image_name: Optional[str] = None


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    image_url: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)