from pydantic import BaseModel
from typing import Optional, List


# 基本模型
class BrandBase(BaseModel):
    name: str
    ecommerce: Optional[str] = None
    shop_id: str


# 創建模型
class BrandCreate(BrandBase):
    pass


# 更新模型
class BrandUpdate(BaseModel):
    name: Optional[str] = None
    ecommerce: Optional[str] = None
    shop_id: Optional[str] = None


# 閱讀模型
class BrandRead(BrandBase):
    id: int

    class Config:
        from_attributes = True
