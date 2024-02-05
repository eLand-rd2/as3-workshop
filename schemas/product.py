from pydantic import BaseModel
from typing import Optional


# Product 基本模型
class ProductBase(BaseModel):
    name: str
    rating: Optional[float] = 3.0
    category: Optional[str] = '保養'



# 用于创建新产品的模型
class ProductCreate(ProductBase):
    brand_id: int


# 用于更新产品的模型
class ProductUpdate(ProductBase):
    name: Optional[str] = None
    rating: Optional[float] = None
    category: Optional[str] = None
    brand_id: Optional[int] = None


# 用于读取产品信息的模型，包含嵌套的 Brand
class ProductRead(ProductBase):
    id: int
    brand: 'BrandBase'

    class Config:  # Pydantic 模型的配置類，用於配置模型的行為
        orm_mode = True # 設置為 True 表示模型可以從 ORM（對象關係映射）對象直接解析
        from_attributes = True # 指示 Pydantic 在創建模型實例時從其他屬性中自動提取數據
