from pydantic import BaseModel
from typing import Optional


# Product 基本模型
class ProductBase(BaseModel):
    name: str
    rating: Optional[float] = 3.0
    categories: Optional[list[str]] = ['保養']
    item_id: str



# 用于创建新产品的模型
class ProductCreate(ProductBase):
    brand_id: int


# 用于更新产品的模型
class ProductUpdate(ProductBase):
    name: Optional[str] = None
    rating: Optional[float] = None
    categories: Optional[str] = None
    brand_id: Optional[int] = None
    item_id: Optional[str] = None


# 用于读取产品信息的模型，包含嵌套的 Brand
class ProductRead(ProductBase):
    id: int
    brand: 'BrandBase'

    class Config:  # Pydantic 模型的配置類，用於配置模型的行為
        from_attributes = True # 指示 Pydantic 在創建模型實例時從其他屬性中自動提取數據
