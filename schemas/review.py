from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ReviewBase(BaseModel):
    text: str
    rating: float
    sentiment: Optional[str] = '中立'
    post_time: datetime


class ReviewCreate(ReviewBase):
    product_id: int


class ReviewUpdate(BaseModel):
    text: Optional[str] = None
    rating: Optional[float] = None
    sentiment: Optional[str] = None
    post_time: Optional[datetime] = None

class ReviewRead(ReviewBase):
    id: int
    product: 'ProductBase'

    class Config:
        from_attributes = True
