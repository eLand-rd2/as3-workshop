import dataclasses
from datetime import datetime
from typing import Optional

from schemas.product import ProductRead


@dataclasses.dataclass
class ReviewsCreate:
    product: 'ProductRead'
    text: str
    rating: float
    post_time: datetime
    sentiment: Optional[str] = '中立'
    topics: Optional[list[str]] = None

    # validate rating, should be float and between 1 and 5
    def __post_init__(self):
        if not (isinstance(self.rating, float) and self.rating in range(1, 6)):
            raise ValueError("Rating must be a float between 1 and 5")
        if not (isinstance(self.post_time, datetime)):
            raise ValueError("Post time must be a datetime object")


@dataclasses.dataclass
class ReviewsUpdate:
    id: int
    text: str
    topics: Optional[list[str]] = None
    sentiment: Optional[str] = '中立'
