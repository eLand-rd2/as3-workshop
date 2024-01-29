from pydantic import BaseModel
from typing import Optional


# Product 基本模型
class ProductBase(BaseModel):
    name: str
    rating: Optional[float] = 3.0


# 用于创建新产品的模型
class ProductCreate(ProductBase):
    brand_id: int


# 用于更新产品的模型
class ProductUpdate(ProductBase):
    name: Optional[str] = None
    rating: Optional[float] = None
    brand_id: Optional[int] = None


# 用于读取产品信息的模型，包含嵌套的 Brand
class ProductRead(ProductBase):
    id: int
    brand: 'BrandBase'

    class Config:
        orm_mode = True
        from_attributes = True
