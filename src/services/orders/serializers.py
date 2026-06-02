from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_amount: float
    status: str
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)